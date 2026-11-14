
import { useEffect, useMemo, useRef, useState } from "react";
import { Link, useLocation } from "react-router-dom";
import {
  Search,
  X,
  BookOpen,
  FileText,
  Layers,
  LayoutDashboard,
  ClipboardList,
  Lightbulb,
  UserRound,
  GraduationCap,
  LoaderCircle,
  CornerDownLeft,
} from "lucide-react";

import api from "../services/api";
import "./GlobalSearch.css";

const pages = [
  { title: "Dashboard", path: "/dashboard", category: "Pages", icon: LayoutDashboard },
  { title: "My Courses", path: "/courses", category: "Pages", icon: BookOpen },
  { title: "Learning Materials", path: "/materials", category: "Pages", icon: FileText },
  { title: "Quizzes", path: "/quizzes", category: "Pages", icon: ClipboardList },
  { title: "Quiz History", path: "/quiz-history", category: "Pages", icon: ClipboardList },
  { title: "Recommendations", path: "/recommendations", category: "Pages", icon: Lightbulb },
  { title: "My Profile", path: "/profile", category: "Pages", icon: UserRound },
  { title: "Learning Path", path: "/learning-path", category: "Pages", icon: GraduationCap },
];

function GlobalSearch() {
  const location = useLocation();
  const [query, setQuery] = useState("");
  const [open, setOpen] = useState(false);
  const [loading, setLoading] = useState(false);
  const [searchData, setSearchData] = useState([]);
  const [loaded, setLoaded] = useState(false);
  const [activeIndex, setActiveIndex] = useState(0);

  const searchRef = useRef(null);
  const inputRef = useRef(null);

  // Load real courses, topics, and materials when search is first opened.
  const loadSearchData = async () => {
    if (loaded || loading) return;

    setLoading(true);

    try {
      const [coursesResponse, enrollmentResponse] = await Promise.all([
        api.get("/courses/"),
        api.get("/enrollments/me"),
      ]);

      const courses = coursesResponse.data || [];
      const enrollments = enrollmentResponse.data || [];

      const enrolledIds = enrollments.map(
        (enrollment) => enrollment.course_id
      );

      const results = [];

      courses.forEach((course) => {
        results.push({
          id: `course-${course.id}`,
          title: course.title,
          description: course.description || course.course_code || "Course",
          category: "Courses",
          path: `/courses/${course.id}`,
          icon: BookOpen,
        });
      });

      const enrolledCourses = courses.filter((course) =>
        enrolledIds.includes(course.id)
      );

      const topicGroups = await Promise.all(
        enrolledCourses.map(async (course) => {
          try {
            const topicsResponse = await api.get(
              `/dashboard/course/${course.id}/topics`
            );

            return (topicsResponse.data || []).map((topic) => ({
              course,
              topic,
            }));
          } catch (error) {
            console.error("Unable to load topics for search:", error);
            return [];
          }
        })
      );

      const allTopics = topicGroups.flat();


      // Add topics to search
      allTopics.forEach(({ course, topic }) => {
        results.push({
          id: `topic-${topic.topic_id}`,
          title: topic.topic_title,
          description: course.title,
          category: "Topics",
          path: `/topics/${topic.topic_id}/materials`,
          icon: Layers,
        });
      });

      // Fetch learning materials
      const materialGroups = await Promise.all(
        allTopics.map(async ({ course, topic }) => {
          try {
            const response = await api.get(
              `/learning-materials/topic/${topic.topic_id}`
            );

            return (response.data || []).map((material) => ({
              material,
              course,
              topic,
            }));
          } catch (error) {
            console.error("Unable to load materials for search:", error);
            return [];
          }
        })
      );

      materialGroups.flat().forEach(({ material, course, topic }) => {
        results.push({
          id: `material-${material.id}`,
          title: material.title,
          description: `${course.title} • ${topic.topic_title} • ${
            material.material_type || "Learning Resource"
          }`,
          searchableText: material.content || "",
          category: "Learning Materials",
          path: `/topics/${topic.topic_id}/materials`,
          icon: FileText,
        });
      });

      // Fetch quizzes for enrolled topics
      const quizGroups = await Promise.all(
        allTopics.map(async ({ course, topic }) => {
          try {
            const response = await api.get(
              `/quizzes/topic/${topic.topic_id}`
            );

            return (response.data || []).map((quiz) => ({
              quiz,
              course,
              topic,
            }));
          } catch (error) {
            console.error("Unable to load quizzes for search:", error);
            return [];
          }
        })
      );

      quizGroups.flat().forEach(({ quiz, course, topic }) => {
        results.push({
          id: `quiz-${quiz.id}`,
          title: quiz.title,
          description: `${course.title} • ${topic.topic_title}`,
          searchableText: quiz.description || "",
          category: "Quizzes",
          path: `/quizzes/${quiz.id}/attempt`,
          icon: ClipboardList,
        });
      });

      // Fetch previous quiz attempts
      try {
        const attemptsResponse = await api.get("/quiz-attempts/me");

        (attemptsResponse.data || []).forEach((attempt) => {
          results.push({
            id: `attempt-${attempt.id}`,
            title: attempt.quiz_title || `Quiz #${attempt.quiz_id}`,
            description: `${attempt.course_title || ""} • ${
              attempt.topic_title || ""
            } • Score: ${attempt.score}/${attempt.total_questions}`,
            searchableText: [
              attempt.quiz_title,
              attempt.course_title,
              attempt.topic_title,
              attempt.score,
              attempt.total_questions,
              `${attempt.score}/${attempt.total_questions}`,
            ]
              .filter(Boolean)
              .join(" "),
            category: "Quiz History",
            path: "/quiz-history",
            icon: ClipboardList,
          });
        });
      } catch (error) {
        console.error("Unable to load quiz history for search:", error);
      }

      setSearchData(results);
      setLoaded(true);
    } catch (error) {
      console.error("Unable to load global search data:", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    const handleOutsideClick = (event) => {
      if (searchRef.current && !searchRef.current.contains(event.target)) {
        setOpen(false);
      }
    };

    document.addEventListener("mousedown", handleOutsideClick);

    return () => {
      document.removeEventListener("mousedown", handleOutsideClick);
    };
  }, []);

  useEffect(() => {
    const handleEscape = (event) => {
      if (event.key === "Escape") {
        setOpen(false);
        inputRef.current?.blur();
      }
    };

    window.addEventListener("keydown", handleEscape);

    return () => window.removeEventListener("keydown", handleEscape);
  }, []);


  const filteredResults = useMemo(() => {
    const value = query.trim().toLowerCase();

    if (value.length < 1) return [];

    const pathname = location.pathname;

    let allowedCategories = [];

    if (pathname === "/dashboard") {
      // Dashboard searches everything
      allowedCategories = [
        "Pages",
        "Courses",
        "Topics",
        "Learning Materials",
        "Quizzes",
        "Quiz History",
      ];
    } else if (pathname === "/courses") {
      allowedCategories = ["Courses"];
    } else if (
      pathname === "/materials" ||
      pathname.includes("/materials")
    ) {
      allowedCategories = ["Topics", "Learning Materials"];
    } else if (
      pathname === "/quizzes" ||
      pathname.includes("/attempt")
    ) {
      allowedCategories = ["Quizzes"];
    } else if (pathname === "/quiz-history") {
      allowedCategories = ["Quiz History"];
    } else {
      allowedCategories = ["Pages"];
    }

    const searchableItems =
      pathname === "/dashboard"
        ? [...pages, ...searchData]
        : searchData;

    return searchableItems
      .filter((item) => {
        if (!allowedCategories.includes(item.category)) {
          return false;
        }

        const searchableText = [
          item.title,
          item.description,
          item.searchableText,
          item.category,
        ]
          .filter(Boolean)
          .join(" ")
          .toLowerCase();

        return searchableText.includes(value);
      })
      .slice(0, 10);
  }, [query, searchData, location.pathname]);


  const handleKeyDown = (event) => {
    if (event.key === "ArrowDown" && filteredResults.length) {
      event.preventDefault();
      setActiveIndex((previous) =>
        (previous + 1) % filteredResults.length
      );
    }

    if (event.key === "ArrowUp" && filteredResults.length) {
      event.preventDefault();
      setActiveIndex((previous) =>
        (previous - 1 + filteredResults.length) % filteredResults.length
      );
    }

    if (event.key === "Enter" && filteredResults[activeIndex]) {
      window.location.href = filteredResults[activeIndex].path;
    }
  };

  const handleClear = () => {
    setQuery("");
    setActiveIndex(0);
    inputRef.current?.focus();
  };

  return (
    <div className="global-search" ref={searchRef}>
      <div className={`global-search-box ${open ? "search-focused" : ""}`}>
        <Search size={19} className="global-search-icon" />

        <input
          ref={inputRef}
          type="text"
          value={query}
          placeholder="Search your learning content..."
          aria-label="Search Learnova"
          aria-expanded={open}
          onFocus={() => {
            setOpen(true);
            loadSearchData();
          }}
          onChange={(event) => {
            setQuery(event.target.value);
            setActiveIndex(0);
            setOpen(true);
          }}
          onKeyDown={handleKeyDown}
        />

        {query && (
          <button
            type="button"
            className="global-search-clear"
            onClick={handleClear}
            aria-label="Clear search"
          >
            <X size={17} />
          </button>
        )}

        <span className="search-shortcut">
          <CornerDownLeft size={13} />
        </span>
      </div>

      {open && (
        <div className="global-search-dropdown">
          {!query.trim() && (
            <div className="search-empty-state">
              <Search size={24} />
              <strong>Search Learnova</strong>
              <p>Start typing to explore your learning library.</p>
            </div>
          )}

          {query.trim().length >= 1 && loading && (
            <div className="search-loading">
              <LoaderCircle size={20} className="search-spinner" />
              <span>Getting your search results...</span>
            </div>
          )}

          {query.trim().length >= 1 &&
            !loading &&
            filteredResults.length > 0 && (
              <div className="search-results">
                <div className="search-results-heading">
                  Search Results
                  <span>{filteredResults.length}</span>
                </div>

                {filteredResults.map((result, index) => {
                  const Icon = result.icon || Search;

                  return (
                    <Link
                      key={result.id || result.path}
                      to={result.path}
                      className={`search-result-item ${
                        activeIndex === index ? "result-active" : ""
                      }`}
                      onClick={() => {
                        setOpen(false);
                        setQuery("");
                      }}
                    >
                      <span className="search-result-icon">
                        <Icon size={18} />
                      </span>

                      <span className="search-result-content">
                        <strong>{result.title}</strong>
                        <small>{result.description || result.category}</small>
                      </span>

                      <span className="search-result-category">
                        {result.category}
                      </span>
                    </Link>
                  );
                })}
              </div>
            )}

          {query.trim().length >= 1 &&
            !loading &&
            loaded &&
            filteredResults.length === 0 && (
              <div className="search-empty-state">
                <Search size={24} />
                <strong>No results found</strong>
                <p>Try another course, topic, or keyword.</p>
              </div>
            )}

          {query.trim().length >= 1 && !loaded && !loading && (
            <div className="search-empty-state">
              <p>Search data could not be loaded. Please try again.</p>
              <button type="button" onClick={loadSearchData}>
                Retry
              </button>
            </div>
          )}

          {filteredResults.length > 0 && (
            <div className="search-dropdown-footer">
              Use ↑ ↓ to navigate and Enter to open
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default GlobalSearch;
