
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import DashboardLayout from "../components/DashboardLayout";
import api from "../services/api";
import "./LearningPath.css";

function LearningPath() {
  const [courses, setCourses] = useState([]);
  const [selectedCourse, setSelectedCourse] = useState("");
  const [path, setPath] = useState([]);
  const [loading, setLoading] = useState(false);
  const [coursesLoading, setCoursesLoading] = useState(true);
  const [updatingMaterial, setUpdatingMaterial] = useState(null);
  const [error, setError] = useState("");

  const navigate = useNavigate();

  const totalMaterials = path.reduce(
    (sum, topic) => sum + Number(topic.total_materials || 0),
    0
  );

  const completedMaterials = path.reduce(
    (sum, topic) => sum + Number(topic.completed_materials || 0),
    0
  );

  const courseProgress =
    totalMaterials > 0
      ? Math.round((completedMaterials / totalMaterials) * 100)
      : 0;

  // Fetch enrolled courses
  useEffect(() => {
    const fetchCourses = async () => {
      try {
        setError("");

        const response = await api.get("/enrollments/me");
        const enrolledCourses = response.data;

        setCourses(enrolledCourses);

        if (enrolledCourses.length > 0) {
          setSelectedCourse(
            String(enrolledCourses[0].course_id)
          );
        }
      } catch (err) {
        setError(
          err.response?.data?.detail ||
            "Failed to load enrolled courses."
        );
      } finally {
        setCoursesLoading(false);
      }
    };

    fetchCourses();
  }, []);

  // Fetch learning path
  useEffect(() => {
    if (!selectedCourse) {
      setPath([]);
      return;
    }

    let isMounted = true;

    const fetchPath = async () => {
      try {
        setLoading(true);
        setError("");

        const response = await api.get(
          `/learning-path/course/${selectedCourse}`
        );

        if (isMounted) {
          setPath(response.data.learning_path || []);
        }
      } catch (err) {
        if (isMounted) {
          setPath([]);
          setError(
            err.response?.data?.detail ||
              "Failed to load learning path."
          );
        }
      } finally {
        if (isMounted) {
          setLoading(false);
        }
      }
    };

    fetchPath();

    return () => {
      isMounted = false;
    };
  }, [selectedCourse]);

  // Mark material as completed
  const markMaterialCompleted = async (materialId) => {
    try {
      setUpdatingMaterial(materialId);
      setError("");

      await api.put(
        `/learning-progress/material/${materialId}`,
        { status: "completed" }
      );

      const response = await api.get(
        `/learning-path/course/${selectedCourse}`
      );

      setPath(response.data.learning_path || []);
    } catch (err) {
      setError(
        err.response?.data?.detail ||
          "Failed to update material progress."
      );
    } finally {
      setUpdatingMaterial(null);
    }
  };

  return (
    <DashboardLayout
      title="Personalized Learning Path"
      subtitle="Follow your learning journey topic by topic."
    >
      <div className="learning-path-page">

        {/* Course selector */}
        <section className="learning-path-selector">
          <div>
            <label htmlFor="learning-course">
              Select Course
            </label>

            <select
              id="learning-course"
              value={selectedCourse}
              onChange={(event) =>
                setSelectedCourse(event.target.value)
              }
              disabled={coursesLoading || courses.length === 0}
            >
              {courses.map((course) => (
                <option
                  key={course.course_id}
                  value={course.course_id}
                >
                  {course.course_title ||
                    course.title ||
                    `Course ${course.course_id}`}
                </option>
              ))}
            </select>
          </div>
        </section>

        {/* Loading */}
        {(coursesLoading || loading) && (
          <div className="learning-path-loading">
            Loading your learning journey...
          </div>
        )}

        {/* Error */}
        {error && (
          <p className="learning-path-error" role="alert">
            {error}
          </p>
        )}

        {/* No enrolled courses */}
        {!coursesLoading &&
          courses.length === 0 &&
          !error && (
            <div className="learning-path-empty">
              <h3>No Enrolled Courses</h3>
              <p>
                Enroll in a course to view your personalized
                learning journey here.
              </p>
            </div>
          )}

        {/* Course progress and topic list */}
        {!coursesLoading &&
          !loading &&
          selectedCourse &&
          !error &&
          path.length > 0 && (
            <>
              <section className="course-progress">
                <div className="course-progress-header">
                  <h3>Overall Course Progress</h3>

                  <span className="course-progress-percentage">
                    {courseProgress}%
                  </span>
                </div>

                <div className="progress-bar">
                  <div
                    className="progress-fill"
                    style={{
                      width: `${courseProgress}%`,
                    }}
                  />
                </div>

                <p>
                  {completedMaterials} of {totalMaterials}{" "}
                  learning materials completed
                </p>
              </section>

              <div className="learning-path-section-heading">
                <h2>Your Learning Journey</h2>
                <p>
                  Follow the topics in sequence and complete
                  the learning materials to make progress.
                </p>
              </div>

              <div className="learning-path-list">
                {path.map((topic) => {
                  const status = String(
                    topic.status || "upcoming"
                  ).toLowerCase();

                  const topicMaterials =
                    topic.materials || [];

                  return (
                    <article
                      className="learning-path-topic"
                      key={topic.topic_id}
                    >
                      {/* Topic heading */}
                      <div className={`topic-heading ${status}`}>
                        <span className="topic-status-icon">
                          {status === "completed"
                            ? "✓"
                            : status === "current"
                            ? "●"
                            : "○"}
                        </span>

                        <h3>
                          {topic.sequence_number}.{" "}
                          {topic.topic_title}
                        </h3>

                        <span className="topic-status-label">
                          {status === "completed"
                            ? "Completed"
                            : status === "current"
                            ? "Current Topic"
                            : "Upcoming"}
                        </span>
                      </div>

                      {/* Topic progress */}
                      <div className="topic-progress-info">
                        <span>
                          Materials completed:{" "}
                          <strong>
                            {topic.completed_materials}/
                            {topic.total_materials}
                          </strong>
                        </span>

                        <strong>
                          {topic.completion_percentage || 0}%
                        </strong>
                      </div>

                      <div className="topic-progress-bar">
                        <div
                          className="topic-progress-fill"
                          style={{
                            width: `${Math.min(
                              100,
                              Math.max(
                                0,
                                Number(
                                  topic.completion_percentage || 0
                                )
                              )
                            )}%`,
                          }}
                        />
                      </div>

                      {/* Learning materials */}
                      <h4 className="topic-materials-heading">
                        Learning Materials
                      </h4>

                      {topicMaterials.length === 0 ? (
                        <p className="material-status-text">
                          No learning materials available.
                        </p>
                      ) : (
                        topicMaterials.map((material) => {
                          const isCompleted =
                            material.status === "completed";

                          const isUpdating =
                            updatingMaterial ===
                            material.material_id;

                          return (
                            <div
                              key={material.material_id}
                              className={`learning-path-material ${
                                isCompleted ? "completed" : ""
                              }`}
                            >
                              <div className="learning-path-material-info">
                                <span className="material-status-dot" />

                                <div>
                                  <span>
                                    {material.title}
                                  </span>

                                  <small className="material-status-text">
                                    {isCompleted
                                      ? "Completed"
                                      : material.status?.replaceAll(
                                          "_",
                                          " "
                                        ) || "Not started"}
                                  </small>
                                </div>
                              </div>

                              <div className="learning-path-material-actions">
                                <button
                                  type="button"
                                  className="learning-path-open-button"
                                  onClick={() =>
                                    navigate(
                                      `/topics/${topic.topic_id}/materials`
                                    )
                                  }
                                >
                                  Open Materials
                                </button>

                                {!isCompleted && (
                                  <button
                                    type="button"
                                    className="learning-path-complete-button"
                                    disabled={isUpdating}
                                    onClick={() =>
                                      markMaterialCompleted(
                                        material.material_id
                                      )
                                    }
                                  >
                                    {isUpdating
                                      ? "Updating..."
                                      : "Mark Completed"}
                                  </button>
                                )}
                              </div>
                            </div>
                          );
                        })
                      )}
                    </article>
                  );
                })}
              </div>
            </>
          )}

        {/* No learning path */}
        {!coursesLoading &&
          !loading &&
          selectedCourse &&
          !error &&
          path.length === 0 && (
            <div className="learning-path-empty">
              <h3>No Learning Path Available</h3>
              <p>
                There are no topics available for this course
                yet. Please check again later.
              </p>
            </div>
          )}
      </div>
    </DashboardLayout>
  );
}

export default LearningPath;
