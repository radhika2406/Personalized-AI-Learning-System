import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { Link, useParams } from "react-router-dom";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import rehypeHighlight from "rehype-highlight";
import {
  ArrowLeft,
  ArrowUp,
  BookOpen,
  CheckCircle2,
  ChevronLeft,
  ChevronRight,
  ListTree,
  LoaderCircle,
} from "lucide-react";
import DashboardLayout from "../components/DashboardLayout";
import api from "../services/api";
import "highlight.js/styles/github-dark.css";
import "./LessonReader.css";
function makeSlug(value = "") {
  return value
    .toLowerCase()
    .trim()
    .replace(/[`\*\_\~]/g, "")
    .replace(/[^a-z0-9\s-]/g, "")
    .replace(/\s+/g, "-")
    .replace(/-+/g, "-");
}
function buildHeadings(markdown = "") {
  const usedIds = new Map();
  const headings = [];
  let fence = null;
  markdown.split("\n").forEach((line) => {
    const fenceMatch = line.match(/^\s{0,3}(```+|\~\~\~+)/);
    if (fenceMatch) {
      const marker = fenceMatch[1][0];
      if (!fence) fence = marker;
      else if (fence === marker) fence = null;
      return;
    }
    if (fence) return;
    // Support normal Markdown headings and optional closing hashes.
    const match = line.match(/^\s{0,3}(#{1,3})\s+(.+?)\s*#*\s*$/);
    if (!match) return;
    const title = match[2]
      .replace(/[`\*\_\~]/g, "")
      .trim();
    const baseId = makeSlug(title) || "lesson-section";
    const occurrence = usedIds.get(baseId) || 0;
    usedIds.set(baseId, occurrence + 1);
    headings.push({
      level: match[1].length,
      title,
      id: occurrence ? `${baseId}-${occurrence + 1}` : baseId,
    });
  });
  return headings;
}
function LessonReader() {
  const { topicId, materialId } = useParams();
  const [material, setMaterial] = useState(null);
  const [status, setStatus] = useState("not_started");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [saving, setSaving] = useState(false);
  const [activeHeading, setActiveHeading] = useState("");
  const [readingProgress, setReadingProgress] = useState(0);
  const [showBackToTop, setShowBackToTop] = useState(false);
  const headingRenderIndex = useRef(0);
  const content = material?.content_text || "";
  const lessonTitle = material?.title || "Lesson";
  const headings = useMemo(() => buildHeadings(content), [content]);
  useEffect(() => {
    let active = true;
    async function loadLesson() {
      setLoading(true);
      setError("");
      setMaterial(null);
      try {
        const [materialsResponse, progressResponse] = await Promise.all([
          api.get(`/learning-materials/topic/${topicId}`),
          api
            .get(`/learning-progress/material/${materialId}`)
            .catch((requestError) => {
              if (requestError.response?.status === 404) {
                return { data: { status: "not_started" } };
              }
              throw requestError;
            }),
        ]);
        const materials = Array.isArray(materialsResponse.data)
          ? materialsResponse.data
          : [];
        const found = materials.find(
          (item) => String(item.id) === String(materialId),
        );
        if (!found) {
          throw new Error("This lesson could not be found for the selected topic.");
        }
        if (active) {
          setMaterial(found);
          setStatus(progressResponse.data?.status || "not_started");
        }
      } catch (requestError) {
        if (active) {
          setError(
            requestError.response?.data?.detail ||
              requestError.message ||
              "Unable to load this lesson. Please try again.",
          );
        }
      } finally {
        if (active) setLoading(false);
      }
    }
    loadLesson();
    return () => {
      active = false;
    };
  }, [topicId, materialId]);
  // Track document reading progress and reveal the back-to-top control.
  useEffect(() => {
    let ticking = false;
    const updateScrollState = () => {
      if (ticking) return;
      ticking = true;
      window.requestAnimationFrame(() => {
        const doc = document.documentElement;
        const scrollableHeight = doc.scrollHeight - window.innerHeight;
        const progress = scrollableHeight > 0
          ? (window.scrollY / scrollableHeight) * 100
          : 0;
        setReadingProgress(Math.min(100, Math.max(0, Math.round(progress))));
        setShowBackToTop(window.scrollY > 420);
        ticking = false;
      });
    };
    updateScrollState();
    window.addEventListener("scroll", updateScrollState, { passive: true });
    window.addEventListener("resize", updateScrollState);
    return () => {
      window.removeEventListener("scroll", updateScrollState);
      window.removeEventListener("resize", updateScrollState);
    };
  }, [content]);
  // Highlight the table-of-contents item nearest the top of the reading area.
  useEffect(() => {
    if (!headings.length) {
      setActiveHeading("");
      return undefined;
    }
    const headingElements = headings
      .map((heading) => document.getElementById(heading.id))
      .filter(Boolean);
    if (!headingElements.length) return undefined;
    const observer = new IntersectionObserver(
      (entries) => {
        const visibleEntries = entries
          .filter((entry) => entry.isIntersecting)
          .sort((a, b) => a.boundingClientRect.top - b.boundingClientRect.top);
        if (visibleEntries[0]) {
          setActiveHeading(visibleEntries[0].target.id);
        }
      },
      {
        rootMargin: "-12% 0px -72% 0px",
        threshold: 0,
      },
    );
    headingElements.forEach((element) => observer.observe(element));
    // Set a useful initial active section, including on direct page loads.
    const firstVisible = headingElements.find(
      (element) => element.getBoundingClientRect().top >= 0,
    );
    setActiveHeading(firstVisible?.id || headingElements[0].id);
    return () => observer.disconnect();
  }, [headings, loading]);
  const completeLesson = useCallback(async () => {
    if (saving || status === "completed") return;
    setSaving(true);
    setError("");
    try {
      const response = await api.put(
        `/learning-progress/material/${materialId}`,
        { status: "completed" },
      );
      setStatus(response.data?.status || "completed");
    } catch (requestError) {
      setError(
        requestError.response?.data?.detail ||
          "Unable to save lesson progress. Please try again.",
      );
    } finally {
      setSaving(false);
    }
  }, [materialId, saving, status]);
  const scrollToHeading = useCallback((headingId) => {
    const target = document.getElementById(headingId);
    if (!target) return;
    setActiveHeading(headingId);
    target.scrollIntoView({ behavior: "smooth", block: "start" });
  }, []);
  // Bottom navigation moves between primary sections (h1/h2).
  // Nested h3 items remain available in the table of contents.
  const navigationHeadings = useMemo(
    () => headings.filter((heading) => heading.level <= 2),
    [headings],
  );
  const activeHeadingPosition = headings.findIndex(
    (heading) => heading.id === activeHeading,
  );
  // If a nested h3 is active, use its parent/main section for bottom navigation.
  const activeNavigationIndex = navigationHeadings.reduce(
    (currentIndex, heading, index) => {
      const headingPosition = headings.findIndex(
        (item) => item.id === heading.id,
      );
      return headingPosition <= activeHeadingPosition ? index : currentIndex;
    },
    0,
  );
  const previousHeading = activeNavigationIndex > 0
    ? navigationHeadings[activeNavigationIndex - 1]
    : null;
  const nextHeading = activeNavigationIndex >= 0
    ? navigationHeadings[activeNavigationIndex + 1] || null
    : navigationHeadings[0] || null;
  const moveSection = useCallback((direction) => {
    if (!navigationHeadings.length) return;
    const sections = navigationHeadings
      .map((heading) => ({
        ...heading,
        element: document.getElementById(heading.id),
      }))
      .filter((heading) => heading.element);
    if (!sections.length) return;
    // Determine the section currently occupying the reading position.
    const readingLine = 130;
    let currentIndex = 0;
    sections.forEach((section, index) => {
      if (section.element.getBoundingClientRect().top <= readingLine) {
        currentIndex = index;
      }
    });
    const targetIndex = currentIndex + direction;
    if (targetIndex < 0 || targetIndex >= sections.length) return;
    const target = sections[targetIndex];
    setActiveHeading(target.id);
    target.element.scrollIntoView({ behavior: "smooth", block: "start" });
  }, [navigationHeadings]);
  const markdownComponents = useMemo(() => {
    const headingRenderer = (level) => ({ children, ...props }) => {
      const title = String(children).replace(/[\\`*_~]/g, "").trim();
      const expectedHeading = headings[headingRenderIndex.current];
      headingRenderIndex.current += 1;
      const matchedHeading = expectedHeading &&
        expectedHeading.level === level &&
        expectedHeading.title === title
          ? expectedHeading
          : headings.find((heading) =>
              heading.level === level && heading.title === title
            );
      const id = matchedHeading?.id || makeSlug(title);
      const Tag = `h${level}`;
      return <Tag id={id} {...props}>{children}</Tag>;
    };
    return {
      h1: headingRenderer(1),
      h2: headingRenderer(2),
      h3: headingRenderer(3),
      a: ({ href, children, ...props }) => (
        <a
          href={href}
          target={href?.startsWith("http") ? "_blank" : undefined}
          rel={href?.startsWith("http") ? "noopener noreferrer" : undefined}
          {...props}
        >
          {children}
        </a>
      ),
    };
  }, [headings]);
  const scrollToTop = () => {
    window.scrollTo({ top: 0, behavior: "smooth" });
  };
  headingRenderIndex.current = 0;
  return (
    <DashboardLayout
      title="Lesson Reader"
      subtitle="A focused space for reading and learning."
    >
      <main className="lesson-reader-page">
        <div
          className="lesson-reading-progress"
          role="progressbar"
          aria-label="Lesson reading progress"
          aria-valuemin={0}
          aria-valuemax={100}
          aria-valuenow={readingProgress}
        >
          <span style={{ width: `${readingProgress}%` }} />
        </div>
        <div className="lesson-reader-topbar">
          <Link to={`/topics/${topicId}/materials`} className="lesson-back-link">
            <ArrowLeft size={17} /> Back to learning materials
          </Link>
          <div className="lesson-reader-topbar-right">
            <span className="lesson-reading-percent">{readingProgress}% read</span>
            {status === "completed" && (
              <span className="lesson-done-pill">
                <CheckCircle2 size={15} /> Completed
              </span>
            )}
          </div>
        </div>
        {loading && (
          <div className="lesson-reader-state">
            <LoaderCircle className="materials-spinner" size={32} />
            <h3>Preparing your lesson...</h3>
          </div>
        )}
        {!loading && error && (
          <div className="lesson-reader-error" role="alert">{error}</div>
        )}
        {!loading && material && (
          <>
            <header className="lesson-reader-hero">
              <span><BookOpen size={16} /> LEARNING MATERIAL</span>
              <h1>{lessonTitle.replace(/\s\*-\s\*Lesson$/i, "")}</h1>
              <p>
                Read at your own pace. Use the contents panel to jump directly to
                any section.
              </p>
              <div className="lesson-reader-meta">
                <span>{headings.length} sections</span>
                <span>Structured notes</span>
              </div>
            </header>
            {!content.trim() && (
              <div className="lesson-reader-error" role="status">
                The lesson record was found, but it does not contain readable
                lesson text in the `content_text` field.
              </div>
            )}
            <div className="lesson-reader-layout">
              <aside className="lesson-toc">
                <div className="lesson-toc-title">
                  <ListTree size={17} /> On this page
                </div>
                {headings.length ? (
                  <nav aria-label="Lesson table of contents">
                    {headings.map((heading) => (
                      <a
                        key={heading.id}
                        className={`toc-level-${heading.level}${activeHeading === heading.id ? " is-active" : ""}`}
                        href={`#${heading.id}`}
                        onClick={(event) => {
                          event.preventDefault();
                          scrollToHeading(heading.id);
                        }}
                        aria-current={activeHeading === heading.id ? "location" : undefined}
                      >
                        {heading.title}
                      </a>
                    ))}
                  </nav>
                ) : (
                  <p>Section links will appear here.</p>
                )}
              </aside>
              <article className="lesson-article">
                {content.trim() ? (
                  <ReactMarkdown
                    remarkPlugins={[remarkGfm]}
                    rehypePlugins={[rehypeHighlight]}
                    components={markdownComponents}
                  >
                    {content}
                  </ReactMarkdown>
                ) : (
                  <p>Lesson content is not available yet.</p>
                )}
                {navigationHeadings.length > 1 && (
                  <nav className="lesson-section-navigation" aria-label="Lesson section navigation">
                    <button
                      className="lesson-section-button lesson-section-button-previous"
                      type="button"
                      onClick={() => moveSection(-1)}
                      disabled={!previousHeading}
                    >
                      <ChevronLeft size={17} /> Previous section
                    </button>
                    <button
                      className="lesson-section-button lesson-section-button-next"
                      type="button"
                      onClick={() => moveSection(1)}
                      disabled={!nextHeading}
                    >
                      Next section <ChevronRight size={17} />
                    </button>
                  </nav>
                )}
              </article>
            </div>
            <footer className="lesson-reader-footer">
              <div>
                <strong>Finished this lesson?</strong>
                <p>Mark it completed to update your learning progress.</p>
              </div>
              <button
                type="button"
                onClick={completeLesson}
                disabled={status === "completed" || saving}
              >
                {saving ? (
                  <><LoaderCircle size={17} className="materials-spinner" /> Saving...</>
                ) : status === "completed" ? (
                  <><CheckCircle2 size={17} /> Lesson completed</>
                ) : (
                  <><CheckCircle2 size={17} /> Mark lesson as completed</>
                )}
              </button>
            </footer>
          </>
        )}
        {showBackToTop && (
          <button
            type="button"
            className="lesson-back-to-top"
            onClick={scrollToTop}
            aria-label="Back to top"
            title="Back to top"
          >
            <ArrowUp size={19} />
          </button>
        )}
      </main>
    </DashboardLayout>
  );
}
export default LessonReader;
