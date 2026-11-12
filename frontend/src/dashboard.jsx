import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import {
  BookOpen,
  FileText,
  ClipboardList,
  Lightbulb,
  ArrowRight,
  GraduationCap,
  BookMarked,
  Target,
} from "lucide-react";

import DashboardLayout from "./components/DashboardLayout";
import api from "./services/api";
import QuizPerformanceChart from "./components/QuizPerformanceChart";
import "./Dashboard.css";

function Dashboard() {
  const [stats, setStats] = useState(null);
  const [myCourses, setMyCourses] = useState([]);

  const [loading, setLoading] = useState(true);
  const [coursesLoading, setCoursesLoading] = useState(true);

  const [error, setError] = useState("");
  const [coursesError, setCoursesError] = useState("");

  // Fetch dashboard statistics
  useEffect(() => {
    const fetchDashboard = async () => {
      try {
        const response = await api.get("/dashboard/me");
        setStats(response.data);
      } catch (err) {
        setError(
          err.response?.data?.detail ||
            "Unable to load dashboard data."
        );
      } finally {
        setLoading(false);
      }
    };

    fetchDashboard();
  }, []);

  // Fetch enrolled courses
  useEffect(() => {
    const fetchMyCourses = async () => {
      try {
        const [enrollmentResponse, coursesResponse] =
          await Promise.all([
            api.get("/enrollments/me"),
            api.get("/courses/"),
          ]);

        const enrolledCourseIds = enrollmentResponse.data.map(
          (enrollment) => enrollment.course_id
        );

        const enrolledCourses = coursesResponse.data.filter(
          (course) => enrolledCourseIds.includes(course.id)
        );

        setMyCourses(enrolledCourses);
      } catch (err) {
        setCoursesError(
          err.response?.data?.detail ||
            "Unable to load your courses."
        );
      } finally {
        setCoursesLoading(false);
      }
    };

    fetchMyCourses();
  }, []);

  // Dashboard statistics configuration

const statCards = stats
  ? [
      {
        title: "Enrolled Courses",
        value: stats.enrolled_courses,
        icon: BookOpen,
        color: "purple",
        description: "Your learning spaces",
      },
      {
        title: "Materials Completed",
        value: stats.learning_materials_completed,
        icon: FileText,
        color: "blue",
        description: "Resources completed",
      },
      {
        title: "Quizzes Attempted",
        value: stats.quizzes_attempted,
        icon: ClipboardList,
        color: "pink",
        description: "Your practice activity",
      },
      {
        title: "Average Quiz Score",
        value:
          stats.average_quiz_percentage != null
            ? `${stats.average_quiz_percentage}%`
            : "—",
        icon: Target,
        color: "orange",
        description: "Across your quiz attempts",
      },
    ]
  : [];


  return (
    <DashboardLayout
      title="Dashboard"
      subtitle="Track your learning journey and progress."
    >
      {/* Welcome Section */}
      <section className="welcome-banner">
        <div className="welcome-content">
          <span className="welcome-eyebrow">
            YOUR LEARNING SPACE
          </span>

          <h2>Welcome to Learnova!</h2>

          <p>
            Every step forward brings you closer to your goals.
            Continue learning and make today count.
          </p>

          <Link to="/courses" className="welcome-button">
            Explore Courses
            <ArrowRight size={17} />
          </Link>
        </div>

        <div className="welcome-illustration">
          <div className="welcome-icon-circle">
            <GraduationCap size={62} strokeWidth={1.5} />
          </div>
          <div className="welcome-decoration decoration-one" />
          <div className="welcome-decoration decoration-two" />
        </div>
      </section>

      {/* Dashboard Statistics */}
      <section className="dashboard-section">
        <div className="dashboard-section-heading">
          <div>
            <span className="section-eyebrow">
              YOUR PERFORMANCE
            </span>
            <h2>Learning Statistics</h2>
            <p>Keep track of your learning achievements.</p>
          </div>
        </div>

        {loading && (
          <div className="dashboard-state">
            Loading your statistics...
          </div>
        )}

        {error && (
          <div className="dashboard-error dashboard-state">
            {error}
          </div>
        )}

        {!loading && !error && stats && (
          <div className="stats-grid">
            {statCards.map((item) => {
              const Icon = item.icon;

              return (
            
              <article
                className={`stat-card stat-card-${item.color}`}
                key={item.title}
              >
                <div className="stat-card-top">
                  <div className={`stat-icon ${item.color}`}>
                    <Icon size={23} strokeWidth={1.8} />
                  </div>

                  <span className="stat-card-accent" aria-hidden="true">
                    ✦
                  </span>
                </div>

                <div className="stat-card-content">
                  <p>{item.title}</p>
                  <h2>{item.value ?? "—"}</h2>
                  <span className="stat-card-description">
                    {item.description}
                  </span>
                </div>
              </article>

              );
            })}
          </div>
        )}
      </section>

      {/* Learning Overview */}
      <section className="progress-overview dashboard-section">
        <div className="dashboard-section-heading">
          <div>
            <span className="section-eyebrow">
              LEARNING INSIGHTS
            </span>
            <h2>Learning Overview</h2>
            <p>A snapshot of your learning progress.</p>
          </div>
        </div>

        {!loading && !error && stats && (
          
        <div className="overview-grid">
          <article className="overview-stat-card topics-card">
            <div className="overview-card-top">
              <div className="overview-icon">
                <BookMarked size={22} />
              </div>
              <span className="overview-tag">LEARNING</span>
            </div>

            <div className="overview-details">
              <strong>{stats.topics_tracked ?? "—"}</strong>
              <h3>Topics Tracked</h3>
              <p>Topics in your learning journey</p>
            </div>
          </article>

          <article className="overview-stat-card mastery-card">
            <div className="overview-card-top">
              <div className="overview-icon">
                <Target size={22} />
              </div>
              <span className="overview-tag">MASTERY</span>
            </div>

            <div className="overview-details">
              <strong>
                {stats.average_topic_mastery != null
                  ? `${stats.average_topic_mastery}%`
                  : "—"}
              </strong>

              <h3>Average Topic Mastery</h3>

              {stats.average_topic_mastery != null && (
                <div
                  className="mastery-progress-track"
                  role="progressbar"
                  aria-label="Average topic mastery"
                  aria-valuemin={0}
                  aria-valuemax={100}
                  aria-valuenow={Math.min(
                    100,
                    Math.max(0, Number(stats.average_topic_mastery) || 0)
                  )}
                >
                  <div
                    className="mastery-progress-fill"
                    style={{
                      width: `${Math.min(
                        100,
                        Math.max(0, Number(stats.average_topic_mastery) || 0)
                      )}%`,
                    }}
                  />
                </div>
              )}

              <p>Your current mastery level</p>
            </div>
          </article>
        </div>

        )}

      </section>

      <QuizPerformanceChart />

      {/* My Courses */}
      <section className="my-courses-section dashboard-section">
        <div className="dashboard-section-heading courses-heading">
          <div>
            <span className="section-eyebrow">
              CONTINUE LEARNING
            </span>
            <h2>My Courses</h2>
            <p>Access your enrolled courses and learning materials.</p>
          </div>

          <Link to="/courses" className="view-all-link">
            View all courses
            <ArrowRight size={16} />
          </Link>
        </div>

        {coursesLoading && (
          <div className="dashboard-state">
            Loading your courses...
          </div>
        )}

        {coursesError && (
          <div className="dashboard-error dashboard-state">
            {coursesError}
          </div>
        )}

        {!coursesLoading &&
          !coursesError &&
          myCourses.length === 0 && (
            <div className="empty-courses">
              <div className="empty-courses-icon">
                <BookOpen size={30} />
              </div>

              <h3>No courses yet</h3>

              <p>
                You haven't enrolled in any courses.
                Explore the available courses to get started.
              </p>

              <Link to="/courses" className="empty-courses-button">
                Explore Courses
                <ArrowRight size={16} />
              </Link>
            </div>
          )}

        {!coursesLoading &&
          !coursesError &&
          myCourses.length > 0 && (
            <div className="my-courses-list">
              {myCourses.map((course) => (
                <article
                  className="my-course-card"
                  key={course.id}
                >
                  <div className="course-card-icon">
                    <BookOpen size={23} />
                  </div>

                  <div className="course-card-content">
                    <span className="course-code">
                      {course.course_code || "ENROLLED COURSE"}
                    </span>

                    <h3>{course.title}</h3>

                    <p>
                      {course.description ||
                        "No description available."}
                    </p>

                    <Link
                      to={`/courses/${course.id}`}
                      className="course-open-link"
                    >
                      View Course
                      <ArrowRight size={16} />
                    </Link>
                  </div>
                </article>
              ))}
            </div>
          )}
      </section>
    </DashboardLayout>
  );
}

export default Dashboard;
