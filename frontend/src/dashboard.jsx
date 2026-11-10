import { useEffect, useState } from "react";
import { NavLink, useNavigate } from "react-router-dom";
import DashboardLayout from "./components/DashboardLayout";
import {
  LayoutDashboard,
  BookOpen,
  FileText,
  ClipboardList,
  Lightbulb,
  UserRound,
  LogOut,
} from "lucide-react";
import api from "./services/api";
import "./Dashboard.css";

function Dashboard() {
  const [stats, setStats] = useState(null);
  const [myCourses, setMyCourses] = useState([]);
  const [coursesLoading, setCoursesLoading] = useState(true);
  const [coursesError, setCoursesError] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    const fetchDashboard = async () => {
      try {
        const response = await api.get("/dashboard/me");
        setStats(response.data);
      } catch (err) {
        setError(
          err.response?.data?.detail ||
          "Unable to load dashboard data"
        );
      } finally {
        setLoading(false);
      }
    };

    fetchDashboard();
  }, []);

  
useEffect(() => {
  const fetchMyCourses = async () => {
    try {
      const [enrollmentResponse, coursesResponse] = await Promise.all([
        api.get("/enrollments/me"),
        api.get("/courses/"),
      ]);

      const enrolledCourseIds = enrollmentResponse.data.map(
        (enrollment) => enrollment.course_id
      );

      const enrolledCourses = coursesResponse.data.filter((course) =>
        enrolledCourseIds.includes(course.id)
      );

      setMyCourses(enrolledCourses);
    } catch (err) {
      setCoursesError(
        err.response?.data?.detail || "Unable to load your courses"
      );
    } finally {
      setCoursesLoading(false);
    }
  };

  fetchMyCourses();
}, []);


  const handleLogout = () => {
    localStorage.removeItem("token");
    navigate("/login");
  };

  const navigation = [
    { name: "Dashboard", path: "/dashboard", icon: LayoutDashboard },
    { name: "My Courses", path: "/courses", icon: BookOpen },
    { name: "Learning Materials", path: "/materials", icon: FileText },
    { name: "Quizzes", path: "/quizzes", icon: ClipboardList },
    {
      name: "Quiz History",
      path: "/quiz-history",
      icon: ClipboardList,
    },
    { name: "Recommendations", path: "/recommendations", icon: Lightbulb },
    { name: "My Profile", path: "/profile", icon: UserRound },
    
  ];

    return (
      <DashboardLayout
        title="Dashboard"
        subtitle="Track your learning journey and progress."
      >
        {loading && <p>Loading dashboard...</p>}

        {error && <p className="dashboard-error">{error}</p>}

        {stats && (
          <>
            <section className="welcome-banner">
              <div>
                <h2>Welcome to Learnova!</h2>
                <p>Your personalized learning journey starts here.</p>
              </div>
              <BookOpen size={55} />
            </section>

            <section className="stats-grid">
              <div className="stat-card">
                <div className="stat-icon red">
                  <BookOpen size={22} />
                </div>
                <p>Enrolled Courses</p>
                <h2>{stats.enrolled_courses}</h2>
              </div>

              <div className="stat-card">
                <div className="stat-icon pink">
                  <FileText size={22} />
                </div>
                <p>Materials Completed</p>
                <h2>{stats.learning_materials_completed}</h2>
              </div>

              <div className="stat-card">
                <div className="stat-icon orange">
                  <ClipboardList size={22} />
                </div>
                <p>Quizzes Attempted</p>
                <h2>{stats.quizzes_attempted}</h2>
              </div>

              <div className="stat-card">
                <div className="stat-icon purple">
                  <Lightbulb size={22} />
                </div>
                <p>Average Quiz Score</p>
                <h2>{stats.average_quiz_percentage}%</h2>
              </div>
            </section>

            <section className="progress-overview">
              <div className="section-heading">
                <h2>Learning Overview</h2>
              </div>

              <div className="overview-card">
                <div className="overview-item">
                  <span>Topics Tracked</span>
                  <strong>{stats.topics_tracked}</strong>
                </div>

                <div className="overview-item">
                  <span>Average Topic Mastery</span>
                  <strong>{stats.average_topic_mastery}%</strong>
                </div>
              </div>
            </section>

            <section className="my-courses-section">
              <h2>My Courses</h2>

              {coursesLoading && <p>Loading your courses...</p>}

              {coursesError && (
                <p className="dashboard-error">{coursesError}</p>
              )}

              {!coursesLoading && !coursesError && myCourses.length === 0 && (
                <p>You haven't enrolled in any courses yet.</p>
              )}

              {!coursesLoading && myCourses.length > 0 && (
                <div className="my-courses-list">
                  {myCourses.map((course) => (
                    <div className="my-course-card" key={course.id}>
                      <h3>{course.title}</h3>
                      <p>{course.course_code}</p>
                      <p>{course.description || "No description available."}</p>
                    </div>
                  ))}
                </div>
              )}
            </section>
          </>
        )}
      </DashboardLayout>
    );

}

export default Dashboard;
