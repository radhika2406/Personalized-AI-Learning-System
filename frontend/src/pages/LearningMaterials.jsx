import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import {
  BookOpen,
  FileText,
  GraduationCap,
  CheckCircle2,
  Circle,
  Layers,
  LoaderCircle,
  ArrowRight,
  ExternalLink,
} from "lucide-react";
import DashboardLayout from "../components/DashboardLayout";
import api from "../services/api";
import "./LearningMaterials.css";

function LearningMaterials() {
  const { topicId } = useParams();
  const navigate = useNavigate();
  const [groups, setGroups] = useState([]);
  const [progress, setProgress] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [updatingId, setUpdatingId] = useState(null);

  useEffect(() => {
    let active = true;

    async function load() {
      setLoading(true);
      setError("");

      try {
        let nextGroups = [];

        if (topicId) {
          const response = await api.get(`/learning-materials/topic/${topicId}`);
          nextGroups = [
            {
              courseTitle: "Learning Materials",
              topicTitle: "Selected Topic",
              topicId,
              materials: response.data,
            },
          ];
        } else {
          const [enrollments, courses] = await Promise.all([
            api.get("/enrollments/me"),
            api.get("/courses/"),
          ]);

          const enrolledIds = enrollments.data.map((item) => item.course_id);
          const enrolledCourses = courses.data.filter((course) =>
            enrolledIds.includes(course.id)
          );

          const nestedGroups = await Promise.all(
            enrolledCourses.map(async (course) => {
              const topicsResponse = await api.get(
                `/dashboard/course/${course.id}/topics`
              );

              return Promise.all(
                topicsResponse.data.map(async (topic) => {
                  const materialsResponse = await api.get(
                    `/learning-materials/topic/${topic.topic_id}`
                  );

                  return {
                    courseTitle: course.title,
                    topicTitle: topic.topic_title,
                    topicId: topic.topic_id,
                    materials: materialsResponse.data,
                  };
                })
              );
            })
          );

          nextGroups = nestedGroups.flat();
        }

        if (!active) return;
        setGroups(nextGroups);

        const allMaterials = nextGroups.flatMap((group) => group.materials);
        const progressResults = await Promise.all(
          allMaterials.map(async (material) => {
            try {
              const response = await api.get(
                `/learning-progress/material/${material.id}`
              );
              return [material.id, response.data.status];
            } catch (requestError) {
              if (requestError.response?.status === 404) {
                return [material.id, "not_started"];
              }
              throw requestError;
            }
          })
        );

        if (active) setProgress(Object.fromEntries(progressResults));
      } catch (requestError) {
        if (active) {
          setError(
            requestError.response?.data?.detail ||
              "Unable to load learning materials."
          );
        }
      } finally {
        if (active) setLoading(false);
      }
    }

    load();
    return () => {
      active = false;
    };
  }, [topicId]);

  async function markComplete(materialId) {
    setUpdatingId(materialId);
    setError("");

    try {
      const response = await api.put(
        `/learning-progress/material/${materialId}`,
        { status: "completed" }
      );
      setProgress((current) => ({
        ...current,
        [materialId]: response.data.status,
      }));
    } catch (requestError) {
      setError(
        requestError.response?.data?.detail ||
          "Unable to update learning progress."
      );
    } finally {
      setUpdatingId(null);
    }
  }

  const allMaterials = groups.flatMap((group) => group.materials);
  const completedCount = allMaterials.filter(
    (material) => progress[material.id] === "completed"
  ).length;
  const completionPercentage = allMaterials.length
    ? Math.round((completedCount / allMaterials.length) * 100)
    : 0;

  function openMaterial(group, material) {
    const type = material.material_type?.toLowerCase();

    if (type === "lesson") {
      navigate(
        `/topics/${group.topicId}/materials/${material.id}/read`,
        { state: { material, topicTitle: group.topicTitle, courseTitle: group.courseTitle } }
      );
      return;
    }

    if (material.content_url) {
      window.open(material.content_url, "_blank", "noopener,noreferrer");
    }
  }

  return (
    <DashboardLayout
      title="Learning Materials"
      subtitle="Explore your course materials and track your learning progress."
    >
      <main className="learning-materials-page">
        <section className="materials-hero">
          <div className="materials-hero-content">
            <span className="materials-eyebrow">
              <GraduationCap size={16} /> YOUR LEARNING LIBRARY
            </span>
            <h2>
              Learn at your own pace.
              <br />
              Grow with every lesson.
            </h2>
            <p>
              Open a lesson to read it in a clean, structured learning space, or
              access its PDF and video resources.
            </p>
          </div>
          <div className="materials-hero-icon">
            <BookOpen size={58} />
          </div>
        </section>

        <section className="materials-overview">
          <div className="materials-heading">
            <div>
              <span className="materials-section-eyebrow">YOUR PROGRESS</span>
              <h2>Learning Overview</h2>
              <p>A summary of your available learning materials.</p>
            </div>
          </div>

          {!loading && !error && (
            <div className="materials-summary-grid">
              <article className="materials-summary-card">
                <div className="materials-summary-icon">
                  <Layers size={22} />
                </div>
                <span>Total Materials</span>
                <strong>{allMaterials.length}</strong>
                <p>Available learning resources</p>
              </article>
              <article className="materials-summary-card">
                <div className="materials-summary-icon">
                  <CheckCircle2 size={22} />
                </div>
                <span>Completed</span>
                <strong>{completedCount}</strong>
                <p>Materials you've completed</p>
              </article>
              <article className="materials-summary-card">
                <div className="materials-summary-icon">
                  <BookOpen size={22} />
                </div>
                <span>Completion</span>
                <strong>{completionPercentage}%</strong>
                <p>Based on available materials</p>
              </article>
            </div>
          )}
        </section>

        <section className="materials-content-section">
          <div className="materials-heading">
            <div>
              <span className="materials-section-eyebrow">COURSE CONTENT</span>
              <h2>Explore Learning Materials</h2>
              <p>Select a lesson card to open the full notes page.</p>
            </div>
          </div>

          {loading && (
            <div className="materials-state">
              <LoaderCircle size={35} className="materials-spinner" />
              <h3>Loading learning materials...</h3>
              <p>Preparing your learning resources.</p>
            </div>
          )}

          {!loading && error && (
            <div className="materials-error" role="alert">
              <p>{error}</p>
            </div>
          )}

          {!loading && !error && groups.length === 0 && (
            <div className="materials-state">
              <div className="materials-empty-icon">
                <BookOpen size={30} />
              </div>
              <h3>No learning materials available</h3>
              <p>
                Learning resources will appear here when they are added to your
                courses.
              </p>
            </div>
          )}

          {!loading &&
            !error &&
            groups.map((group, index) => (
              <section
                key={`${group.topicId}-${index}`}
                className="materials-topic-section"
              >
                <div className="materials-topic-heading">
                  <div className="materials-topic-heading-icon">
                    <BookOpen size={21} />
                  </div>
                  <div>
                    <span className="materials-course-name">
                      {group.courseTitle}
                    </span>
                    <h3>{group.topicTitle}</h3>
                    <p>
                      {
                        group.materials.filter(
                          (material) => progress[material.id] === "completed"
                        ).length
                      }{" "}
                      of {group.materials.length} materials completed
                    </p>
                  </div>
                </div>

                <div className="materials-grid">
                  {group.materials.map((material) => {
                    const isLesson =
                      material.material_type?.toLowerCase() === "lesson";
                    const isCompleted = progress[material.id] === "completed";
                    const isUpdating = updatingId === material.id;
                    const canOpen = isLesson || Boolean(material.content_url);
                    const typeLabel = material.material_type || "Learning Resource";

                    return (
                      <article
                        key={material.id}
                        className={`material-card ${
                          isCompleted ? "is-completed" : ""
                        } ${isLesson ? "material-card-clickable" : ""}`}
                      >
                        <button
                          type="button"
                          className="material-open-area"
                          onClick={() => openMaterial(group, material)}
                          disabled={!canOpen}
                          aria-label={`${isLesson ? "Read" : "Open"} ${material.title}`}
                        >
                          <div className="material-card-top">
                            <div className="material-file-icon">
                              {isLesson ? (
                                <BookOpen size={24} />
                              ) : (
                                <FileText size={24} />
                              )}
                            </div>
                            {isCompleted ? (
                              <span className="material-status completed">
                                <CheckCircle2 size={14} /> Completed
                              </span>
                            ) : (
                              <span className="material-status pending">
                                <Circle size={13} /> Not Started
                              </span>
                            )}
                          </div>

                          <span className="material-type">{typeLabel}</span>
                          <h4>{material.title}</h4>
                          <p>
                            {isLesson
                              ? "Open the complete notes in a focused reader with headings, examples, code blocks and a table of contents."
                              : material.description ||
                                "Open the attached learning resource."}
                          </p>
                          <span className="material-open-label">
                            {isLesson
                              ? "Read full lesson"
                              : material.content_url
                                ? material.material_type?.toLowerCase() === "pdf"
                                  ? "View PDF"
                                  : "Watch video"
                                : "Resource unavailable"}
                            <ArrowRight size={16} />
                          </span>
                        </button>

                        {material.content_url && !isLesson && (
                          <a
                            className="material-resource-link"
                            href={material.content_url}
                            target="_blank"
                            rel="noopener noreferrer"
                          >
                            Open resource <ExternalLink size={14} />
                          </a>
                        )}

                        <div className="material-card-footer">
                          <button
                            type="button"
                            className={
                              isCompleted
                                ? "material-completed-button"
                                : "material-complete-button"
                            }
                            disabled={isCompleted || isUpdating}
                            onClick={() => markComplete(material.id)}
                          >
                            {isUpdating ? (
                              <>
                                <LoaderCircle
                                  size={16}
                                  className="materials-spinner"
                                />
                                Saving...
                              </>
                            ) : isCompleted ? (
                              <>
                                <CheckCircle2 size={16} /> Completed
                              </>
                            ) : (
                              <>
                                <CheckCircle2 size={16} /> Mark as Completed
                              </>
                            )}
                          </button>
                        </div>
                      </article>
                    );
                  })}
                </div>
              </section>
            ))}
        </section>
      </main>
    </DashboardLayout>
  );
}

export default LearningMaterials;
