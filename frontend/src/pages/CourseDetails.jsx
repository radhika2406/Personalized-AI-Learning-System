import { useEffect, useState } from "react";
import { useParams, useNavigate, Link } from "react-router-dom";
import {
  BookOpen,
  GraduationCap,
  ArrowRight,
  CheckCircle2,
  Circle,
  FileText,
  Target,
  LoaderCircle,
  Sun,
  Moon,
} from "lucide-react";

import api from "../services/api";
import DashboardLayout from "../components/DashboardLayout";
import Logo from "../components/Logo";
import { useTheme } from "../ThemeContext";
import "./CourseDetails.css";

function CourseDetails() {
  const { courseId } = useParams();
  const navigate = useNavigate();
  const { theme, toggleTheme } = useTheme();

  const [course, setCourse] = useState(null);
  const [topics, setTopics] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const [isLoggedIn, setIsLoggedIn] = useState(
    Boolean(localStorage.getItem("token"))
  );
  const [isEnrolled, setIsEnrolled] = useState(false);
  const [progressAvailable, setProgressAvailable] = useState(false);
  const [enrolling, setEnrolling] = useState(false);

  useEffect(() => {
    let isMounted = true;

    const fetchCourseDetails = async () => {
      setLoading(true);
      setError("");

      const token = localStorage.getItem("token");
      const loggedIn = Boolean(token);

      if (isMounted) {
        setIsLoggedIn(loggedIn);
        setIsEnrolled(false);
        setProgressAvailable(false);
      }

      try {
        // Course and public topics are available to everyone.
        const [courseResponse, topicsResponse] = await Promise.all([
          api.get(`/courses/${courseId}`),
          api.get(`/topics/course/${courseId}`),
        ]);

        if (!isMounted) return;

        setCourse(courseResponse.data);

        // Normalize the public topic response.
        const publicTopics = topicsResponse.data.map((topic) => ({
          ...topic,
          topic_id: topic.id,
          topic_title: topic.title,
          completed_learning_materials: 0,
          total_learning_materials: 0,
          mastery_score: 0,
        }));

        setTopics(publicTopics);

        // Logged-out visitors can stop here.
        if (!loggedIn) return;

        // Check whether the logged-in user is enrolled.
        try {
          await api.get(`/enrollments/courses/${courseId}`);

          if (!isMounted) return;

          setIsEnrolled(true);

          // Only enrolled users can access personalized progress.
          try {
            const progressResponse = await api.get(
              `/dashboard/course/${courseId}/topics`
            );

            if (!isMounted) return;

            setTopics(progressResponse.data);
            setProgressAvailable(true);
          } catch (progressError) {
            console.error(
              "Unable to load course progress:",
              progressError
            );
          }
        } catch (enrollmentError) {
          if (
            enrollmentError.response?.status !== 404 &&
            enrollmentError.response?.status !== 403
          ) {
            console.error(
              "Unable to check course enrollment:",
              enrollmentError
            );
          }
        }
      } catch (err) {
        if (!isMounted) return;

        setError(
          err.response?.data?.detail ||
            "Unable to load course details. Please try again."
        );
      } finally {
        if (isMounted) {
          setLoading(false);
        }
      }
    };

    fetchCourseDetails();

    return () => {
      isMounted = false;
    };
  }, [courseId]);

  const handleEnroll = async () => {
    const token = localStorage.getItem("token");

    if (!token) {
      navigate("/login", {
        state: {
          from: {
            pathname: `/courses/${courseId}`,
          },
          enrollmentIntent: true,
        },
      });
      return;
    }

    setEnrolling(true);
    setError("");

    try {
      await api.post(`/enrollments/courses/${courseId}`);

      setIsLoggedIn(true);
      setIsEnrolled(true);

      const progressResponse = await api.get(
        `/dashboard/course/${courseId}/topics`
      );

      setTopics(progressResponse.data);
      setProgressAvailable(true);
    } catch (err) {
      if (err.response?.status === 409) {
        // The user may already be enrolled.
        try {
          const progressResponse = await api.get(
            `/dashboard/course/${courseId}/topics`
          );

          setIsEnrolled(true);
          setTopics(progressResponse.data);
          setProgressAvailable(true);
        } catch {
          setError(
            "You are already enrolled, but your learning progress could not be loaded."
          );
        }
      } else {
        setError(
          err.response?.data?.detail ||
            "Unable to enroll in this course. Please try again."
        );
      }
    } finally {
      setEnrolling(false);
    }
  };

  const handleTopicClick = (topicId) => {
    if (!isLoggedIn) {
      navigate("/login");
      return;
    }

    if (!isEnrolled) {
      return;
    }

    navigate(`/topics/${topicId}/materials`);
  };

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

  const pageContent = (
    <main className="course-details-page">
      {loading && (
        <div className="course-details-state">
          <LoaderCircle
            size={35}
            className="course-details-spinner"
          />
          <h3>Loading course details...</h3>
          <p>Preparing your course and topic information.</p>
        </div>
      )}

      {!loading && error && !course && (
        <div className="course-details-error" role="alert">
          <p>{error}</p>
          <button
            onClick={() =>
              navigate(isLoggedIn ? "/courses" : "/")
            }
          >
            Go Back
          </button>
        </div>
      )}

      {!loading && course && (
        <>
          <section className="course-details-hero">
            <div className="course-details-hero-content">
              <span className="course-details-eyebrow">
                <GraduationCap size={16} />
                {isEnrolled
                  ? "YOUR LEARNING JOURNEY"
                  : "EXPLORE LEARNOVA"}
              </span>

              <span className="course-details-code">
                {course.course_code}
              </span>

              <h2>{course.title}</h2>

              <p>
                {course.description ||
                  "Explore the topics and learning materials in this course."}
              </p>

              <div className="course-details-actions">
                <button
                  className="course-back-button"
                  onClick={() =>
                    navigate(isLoggedIn ? "/courses" : "/")
                  }
                >
                  <ArrowRight
                    size={16}
                    className="back-arrow"
                  />
                  {isLoggedIn ? "Back to My Courses" : "Back to Home"}
                </button>

                {!isEnrolled && (
                  <button
                    className="course-enroll-button"
                    onClick={handleEnroll}
                    disabled={enrolling}
                  >
                    {enrolling
                      ? "Enrolling..."
                      : "Enroll Now"}
                    {!enrolling && <ArrowRight size={17} />}
                  </button>
                )}

                {isEnrolled && (
                  <button
                    className="course-enroll-button"
                    onClick={() => navigate("/materials")}
                  >
                    Continue Learning
                    <ArrowRight size={17} />
                  </button>
                )}
              </div>
            </div>

            <div className="course-details-hero-icon">
              <BookOpen size={58} strokeWidth={1.5} />
            </div>
          </section>

          {error && (
            <div className="course-details-error" role="alert">
              <p>{error}</p>
            </div>
          )}

          {isEnrolled && progressAvailable ? (
            <section className="course-progress-section">
              <div className="course-details-section-heading">
                <div>
                  <span className="course-details-section-eyebrow">
                    YOUR PERFORMANCE
                  </span>
                  <h2>Learning Overview</h2>
                  <p>
                    Your course activity and topic mastery.
                  </p>
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
          ) : (
            <section className="course-progress-section">
              <div className="course-details-section-heading">
                <div>
                  <span className="course-details-section-eyebrow">
                    COURSE OVERVIEW
                  </span>
                  <h2>What You'll Learn</h2>
                  <p>
                    Explore the topics included in this course.
                    Enroll to start tracking your learning progress.
                  </p>
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
              </div>
            </section>
          )}

          <section className="course-topics-section">
            <div className="course-details-section-heading">
              <div>
                <span className="course-details-section-eyebrow">
                  COURSE CONTENT
                </span>
                <h2>Explore Course Topics</h2>
                <p>
                  {isEnrolled
                    ? "Select a topic to continue your learning."
                    : "Explore the topics covered in this course."}
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
                  Topics for this course will appear here when
                  available.
                </p>
              </div>
            ) : (
              <div className="course-topics-list">
                {topics.map((topic) => {
                  const topicId = topic.topic_id ?? topic.id;
                  const topicTitle =
                    topic.topic_title ?? topic.title;

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
                      className={`course-topic-card ${
                        isEnrolled ? "" : "course-topic-preview"
                      }`}
                      key={topicId}
                      onClick={() => handleTopicClick(topicId)}
                      role="button"
                      tabIndex={0}
                      onKeyDown={(event) => {
                        if (
                          event.key === "Enter" ||
                          event.key === " "
                        ) {
                          event.preventDefault();
                          handleTopicClick(topicId);
                        }
                      }}
                      aria-label={
                        isEnrolled
                          ? `Open ${topicTitle} learning materials`
                          : `${topicTitle} topic preview`
                      }
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
                        {topic.sequence_number}. {topicTitle}
                      </h3>

                      {topic.description && (
                        <p className="course-topic-description">
                          {topic.description}
                        </p>
                      )}

                      {isEnrolled ? (
                        <>
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
                                aria-label={`${topicTitle} mastery`}
                              >
                                <div
                                  className="topic-progress-fill"
                                  style={{
                                    width: `${safeMastery}%`,
                                  }}
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
                        </>
                      ) : (
                        <div className="course-topic-footer">
                          <BookOpen size={16} />
                          {isLoggedIn
                            ? "Enroll to access learning materials"
                            : "Enroll to start learning"}
                        </div>
                      )}
                    </article>
                  );
                })}
              </div>
            )}
          </section>
        </>
      )}
    </main>
  );

  // Logged-in users retain the existing dashboard layout.
  if (isLoggedIn) {
    return (
      <DashboardLayout
        title="Course Details"
        subtitle="Explore topics and track your learning progress."
      >
        {pageContent}
      </DashboardLayout>
    );
  }

  // Public visitors get a simple header without the dashboard sidebar.
  return (
    <div
      className="public-course-layout"
      data-theme={theme}
    >
      <header className="public-course-header">
        <Link to="/" className="public-course-brand">
          <Logo />
        </Link>

        <div className="public-course-header-actions">
          <button
            type="button"
            className="theme-toggle"
            onClick={toggleTheme}
            aria-label="Toggle theme"
          >
            {theme === "dark" ? (
              <Sun size={20} />
            ) : (
              <Moon size={20} />
            )}
          </button>

          <Link to="/login" className="public-course-login">
            Log In
          </Link>

          <Link
            to="/register"
            className="public-course-register"
          >
            Get Started
          </Link>
        </div>
      </header>

      <div className="public-course-content">
        {pageContent}
      </div>
    </div>
  );
}

export default CourseDetails;