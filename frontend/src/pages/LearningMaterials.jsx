import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import {
  BookOpen,
  FileText,
  GraduationCap,
  CheckCircle2,
  Circle,
  Layers,
  LoaderCircle,
} from "lucide-react";

import DashboardLayout from "../components/DashboardLayout";
import api from "../services/api";
import "./LearningMaterials.css";

function LearningMaterials() {
  const { topicId } = useParams();

  const [groups, setGroups] = useState([]);
  const [progress, setProgress] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [updatingId, setUpdatingId] = useState(null);

  useEffect(() => {
    let isMounted = true;

    const fetchMaterials = async () => {
      setLoading(true);
      setError("");

      try {
        let materialGroups = [];

        // Mode 1: Materials of one selected topic
        if (topicId) {
          const response = await api.get(
            `/learning-materials/topic/${topicId}`
          );

          materialGroups = [
            {
              courseTitle: "Learning Materials",
              topicTitle: "Selected Topic",
              materials: response.data,
            },
          ];
        } else {
          // Mode 2: Materials across enrolled courses
          const [enrollmentResponse, coursesResponse] =
            await Promise.all([
              api.get("/enrollments/me"),
              api.get("/courses/"),
            ]);

          const enrolledCourseIds =
            enrollmentResponse.data.map(
              (enrollment) => enrollment.course_id
            );

          const enrolledCourses =
            coursesResponse.data.filter((course) =>
              enrolledCourseIds.includes(course.id)
            );

          materialGroups = await Promise.all(
            enrolledCourses.map(async (course) => {
              const topicsResponse = await api.get(
                `/dashboard/course/${course.id}/topics`
              );

              const topicGroups = await Promise.all(
                topicsResponse.data.map(async (topic) => {
                  const materialsResponse = await api.get(
                    `/learning-materials/topic/${topic.topic_id}`
                  );

                  return {
                    courseTitle: course.title,
                    topicTitle: topic.topic_title,
                    materials: materialsResponse.data,
                  };
                })
              );

              return topicGroups;
            })
          );

          materialGroups = materialGroups.flat();
        }

        if (!isMounted) return;

        setGroups(materialGroups);

        const allMaterials = materialGroups.flatMap(
          (group) => group.materials
        );

        const progressResults = await Promise.all(
          allMaterials.map(async (material) => {
            try {
              const result = await api.get(
                `/learning-progress/material/${material.id}`
              );

              return [material.id, result.data.status];
            } catch (err) {
              if (err.response?.status === 404) {
                return [material.id, "not_started"];
              }
              throw err;
            }
          })
        );

        if (isMounted) {
          setProgress(Object.fromEntries(progressResults));
        }
      } catch (err) {
        if (isMounted) {
          setError(
            err.response?.data?.detail ||
              "Unable to load learning materials."
          );
        }
      } finally {
        if (isMounted) setLoading(false);
      }
    };

    fetchMaterials();

    return () => {
      isMounted = false;
    };
  }, [topicId]);

  const handleComplete = async (materialId) => {
    setUpdatingId(materialId);
    setError("");

    try {
      const response = await api.put(
        `/learning-progress/material/${materialId}`,
        { status: "completed" }
      );

      setProgress((previous) => ({
        ...previous,
        [materialId]: response.data.status,
      }));
    } catch (err) {
      setError(
        err.response?.data?.detail ||
          "Unable to update learning progress."
      );
    } finally {
      setUpdatingId(null);
    }
  };

  const allMaterials = groups.flatMap(
    (group) => group.materials
  );

  const totalMaterials = allMaterials.length;

  const completedMaterials = allMaterials.filter(
    (material) => progress[material.id] === "completed"
  ).length;

  const completionPercentage =
    totalMaterials > 0
      ? Math.round((completedMaterials / totalMaterials) * 100)
      : 0;

  return (
    <DashboardLayout
      title="Learning Materials"
      subtitle="Explore your course materials and track your learning progress."
    >
      <main className="learning-materials-page">

        {/* Hero */}
        <section className="materials-hero">
          <div className="materials-hero-content">
            <span className="materials-eyebrow">
              <GraduationCap size={16} />
              YOUR LEARNING LIBRARY
            </span>

            <h2>
              Learn at your own pace.
              <br />
              Grow with every lesson.
            </h2>

            <p>
              Access your learning resources, complete materials,
              and keep track of your educational journey.
            </p>
          </div>

          <div className="materials-hero-icon">
            <BookOpen size={58} strokeWidth={1.5} />
          </div>
        </section>

        {/* Summary */}
        <section className="materials-overview">
          <div className="materials-heading">
            <div>
              <span className="materials-section-eyebrow">
                YOUR PROGRESS
              </span>
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
                <strong>{totalMaterials}</strong>
                <p>Available learning resources</p>
              </article>

              <article className="materials-summary-card">
                <div className="materials-summary-icon">
                  <CheckCircle2 size={22} />
                </div>
                <span>Completed</span>
                <strong>{completedMaterials}</strong>
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

        {/* Materials */}
        <section className="materials-content-section">
          <div className="materials-heading">
            <div>
              <span className="materials-section-eyebrow">
                COURSE CONTENT
              </span>
              <h2>Explore Learning Materials</h2>
              <p>
                Open your course resources and mark lessons as completed.
              </p>
            </div>
          </div>

          {loading && (
            <div className="materials-state">
              <LoaderCircle
                size={35}
                className="materials-spinner"
              />
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
                Learning resources will appear here when they are added
                to your courses.
              </p>
            </div>
          )}

          {!loading && !error && groups.length > 0 && (
            <div className="materials-groups">
              {groups.map((group, index) => {
                const groupCompleted = group.materials.filter(
                  (material) =>
                    progress[material.id] === "completed"
                ).length;

                return (
                  <section
                    key={`${group.courseTitle}-${group.topicTitle}-${index}`}
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
                          {groupCompleted} of {group.materials.length}{" "}
                          materials completed
                        </p>
                      </div>
                    </div>

                    {group.materials.length === 0 ? (
                      <div className="materials-group-empty">
                        No materials have been added to this topic yet.
                      </div>
                    ) : (
                      <div className="materials-grid">
                        {group.materials.map((material) => {
                          const isCompleted =
                            progress[material.id] === "completed";

                          const isUpdating =
                            updatingId === material.id;

                          return (
                            <article
                              key={material.id}
                              className={`material-card ${
                                isCompleted ? "is-completed" : ""
                              }`}
                            >
                              <div className="material-card-top">
                                <div className="material-file-icon">
                                  <FileText size={24} />
                                </div>

                                {isCompleted ? (
                                  <span className="material-status completed">
                                    <CheckCircle2 size={14} />
                                    Completed
                                  </span>
                                ) : (
                                  <span className="material-status pending">
                                    <Circle size={13} />
                                    Not Started
                                  </span>
                                )}
                              </div>

                              <span className="material-type">
                                {material.material_type || "Learning Resource"}
                              </span>

                              <h4>{material.title}</h4>

                              <p>
                                {material.content ||
                                  "No additional description available."}
                              </p>

                              <div className="material-card-footer">
                                <button
                                  type="button"
                                  className={
                                    isCompleted
                                      ? "material-completed-button"
                                      : "material-complete-button"
                                  }
                                  disabled={isCompleted || isUpdating}
                                  onClick={() =>
                                    handleComplete(material.id)
                                  }
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
                                      <CheckCircle2 size={16} />
                                      Completed
                                    </>
                                  ) : (
                                    <>
                                      <CheckCircle2 size={16} />
                                      Mark as Completed
                                    </>
                                  )}
                                </button>
                              </div>
                            </article>
                          );
                        })}
                      </div>
                    )}
                  </section>
                );
              })}
            </div>
          )}
        </section>
      </main>
    </DashboardLayout>
  );
}

export default LearningMaterials;
