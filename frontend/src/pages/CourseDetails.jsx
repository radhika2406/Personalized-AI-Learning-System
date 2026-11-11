
import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import {
  BookOpen,
  GraduationCap,
  ArrowRight,
  CheckCircle2,
  Circle,
  FileText,
  Target,
  LoaderCircle,
} from "lucide-react";

import api from "../services/api";
import DashboardLayout from "../components/DashboardLayout";
import "./CourseDetails.css";

function CourseDetails() {
  const { courseId } = useParams();
  const navigate = useNavigate();

  const [course, setCourse] = useState(null);
  const [topics, setTopics] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    let isMounted = true;

    const fetchCourseDetails = async () => {
      setLoading(true);
      setError("");

      try {
        const [courseResponse, topicsResponse] = await Promise.all([
          api.get(`/courses/${courseId}`),
          api.get(`/dashboard/course/${courseId}/topics`),
        ]);

        if (!isMounted) return;

        setCourse(courseResponse.data);
        setTopics(topicsResponse.data);
      } catch (err) {
        if (!isMounted) return;

        setError(
          err.response?.data?.detail ||
            "Unable to load course details. Please try again."
        );
      } finally {
        if (isMounted) setLoading(false);
      }
    };

    fetchCourseDetails();

    return () => {
      isMounted = false;
    };
  }, [courseId]);

  const totalMaterials = topics.reduce(
    (total, topic) =>
      total + (Number(topic.total_learning_materials) || 0),
    0
  );

  const completedMaterials = topics.reduce(
    (total, topic) =>
      total + (Number(topic.completed_learning_materials) || 0),
    0
  );

  const averageMastery =
    topics.length > 0
      ? topics.reduce(
          (total, topic) =>
            total + (Number(topic.mastery_score) || 0),
          0
        ) / topics.length
      : 0;

  return (
    <DashboardLayout
      title="Course Details"
      subtitle="Explore topics and track your learning progress."
    >
      <main className="course-details-page">

        {loading && (
          <div className="course-details-state">
            <LoaderCircle size={35} className="course-details-spinner" />
            <h3>Loading course details...</h3>
            <p>Preparing your course and topic information.</p>
          </div>
        )}

        {!loading && error && (
          <div className="course-details-error" role="alert">
            <p>{error}</p>
            <button onClick={() => navigate("/courses")}>
              Back to My Courses
            </button>
          </div>
        )}

        {!loading && !error && course && (
          <>
            {/* Course hero */}
            <section className="course-details-hero">
              <div className="course-details-hero-content">
                <span className="course-details-eyebrow">
                  <GraduationCap size={16} />
                  YOUR LEARNING JOURNEY
                </span>

                <span className="course-details-code">
                  {course.course_code}
                </span>

                <h2>{course.title}</h2>

                <p>
                  {course.description ||
                    "Explore the topics and learning materials in this course."}
                </p>

                <button
                  className="course-back-button"
                  onClick={() => navigate("/courses")}
                >
                  <ArrowRight size={16} className="back-arrow" />
                  Back to My Courses
                </button>
              </div>

              <div className="course-details-hero-icon">
                <BookOpen size={58} strokeWidth={1.5} />
              </div>
            </section>

            {/* Learning summary */}
            <section className="course-progress-section">
              <div className="course-details-section-heading">
                <div>
                  <span className="course-details-section-eyebrow">
                    YOUR PERFORMANCE
                  </span>
                  <h2>Learning Overview</h2>
                  <p>Your course activity and topic mastery.</p>
                </div>
              </div>

              <div className="course-progress-grid">
                <article className="course-progress-card">
                  <div className="course-progress-icon">
                    <BookOpen size={22} />
                  </div>
                  <span>Total Topics</span>
                  <strong>{topics.length}</strong>
                  <p>Topics in this course</p>
                </article>

                <article className="course-progress-card">
                  <div className="course-progress-icon">
                    <FileText size={22} />
                  </div>
                  <span>Materials Completed</span>
                  <strong>
                    {completedMaterials}/{totalMaterials}
                  </strong>
                  <p>Completed learning materials</p>
                </article>

                <article className="course-progress-card">
                  <div className="course-progress-icon">
                    <Target size={22} />
                  </div>
                  <span>Average Topic Mastery</span>
                  <strong>{averageMastery.toFixed(2)}%</strong>
                  <p>Average across listed topics</p>
                </article>
              </div>
            </section>

            {/* Topics */}
            <section className="course-topics-section">
              <div className="course-details-section-heading">
                <div>
                  <span className="course-details-section-eyebrow">
                    COURSE CONTENT
                  </span>
                  <h2>Explore Course Topics</h2>
                  <p>
                    Select a topic to explore its learning materials.
                  </p>
                </div>

                <span className="course-topic-count">
                  {topics.length} Topics
                </span>
              </div>

              {topics.length === 0 ? (
                <div className="course-details-state">
                  <div className="course-details-empty-icon">
                    <BookOpen size={30} />
                  </div>
                  <h3>No topics available yet</h3>
                  <p>
                    Topics for this course will appear here when available.
                  </p>
                </div>
              ) : (
                <div className="course-topics-list">
                  {topics.map((topic) => {
                    const completed =
                      Number(topic.completed_learning_materials) || 0;

                    const total =
                      Number(topic.total_learning_materials) || 0;

                    const mastery =
                      Number(topic.mastery_score) || 0;

                    const safeMastery = Math.min(
                      100,
                      Math.max(0, mastery)
                    );

                    return (
                      <article
                        className="course-topic-card"
                        key={topic.topic_id}
                        onClick={() =>
                          navigate(
                            `/topics/${topic.topic_id}/materials`
                          )
                        }
                        role="button"
                        tabIndex={0}
                        onKeyDown={(event) => {
                          if (
                            event.key === "Enter" ||
                            event.key === " "
                          ) {
                            event.preventDefault();
                            navigate(
                              `/topics/${topic.topic_id}/materials`
                            );
                          }
                        }}
                        aria-label={`Open ${topic.topic_title} learning materials`}
                      >
                        <div className="course-topic-top">
                          <div className="course-topic-icon">
                            <BookOpen size={23} />
                          </div>

                          <span className="course-topic-sequence">
                            TOPIC {topic.sequence_number}
                          </span>

                          <ArrowRight
                            className="course-topic-arrow"
                            size={19}
                          />
                        </div>

                        <h3>
                          {topic.sequence_number}. {topic.topic_title}
                        </h3>

                        <div className="course-topic-info">
                          <div className="course-topic-materials">
                            <FileText size={16} />
                            <span>Learning Materials</span>
                            <strong>
                              {completed}/{total}
                            </strong>
                          </div>

                          <div className="course-topic-mastery">
                            <div>
                              <span>Topic Mastery</span>
                              <strong>{mastery}%</strong>
                            </div>

                            <div
                              className="topic-progress-track"
                              role="progressbar"
                              aria-valuenow={safeMastery}
                              aria-valuemin={0}
                              aria-valuemax={100}
                              aria-label={`${topic.topic_title} mastery`}
                            >
                              <div
                                className="topic-progress-fill"
                                style={{ width: `${safeMastery}%` }}
                              />
                            </div>
                          </div>
                        </div>

                        <div className="course-topic-footer">
                          {total > 0 && completed >= total ? (
                            <>
                              <CheckCircle2 size={16} />
                              All materials completed
                            </>
                          ) : (
                            <>
                              <Circle size={16} />
                              Continue learning
                            </>
                          )}
                        </div>
                      </article>
                    );
                  })}
                </div>
              )}
            </section>
          </>
        )}
      </main>
    </DashboardLayout>
  );
}

export default CourseDetails;
