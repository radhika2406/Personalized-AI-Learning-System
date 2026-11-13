import { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import {
  ArrowRight,
  BookOpen,
  Brain,
  ChartNoAxesCombined,
  CheckCircle2,
  GraduationCap,
  Layers3,
  Menu,
  Moon,
  Sun,
  Target,
  X,
  Code2,
  Network,
} from "lucide-react";

import { useTheme } from "../ThemeContext";
import LearnovaIntro from "../components/intro/LearnovaIntro";
import api from "../services/api";
import "./Home.css";

function Home({ showIntro, onIntroComplete }) {
  const { theme, toggleTheme } = useTheme();
  const navigate = useNavigate();

const handleLogout = () => {
  localStorage.removeItem("token");

  setAccount(null);
  setStats(null);
  setMyCourses([]);
  setMenuOpen(false);

  navigate("/", { replace: true });
};
  const [account, setAccount] = useState(null);
  const [stats, setStats] = useState(null);
  const [courses, setCourses] = useState([]);
  const [myCourses, setMyCourses] = useState([]);
  const [loading, setLoading] = useState(false);
  const [menuOpen, setMenuOpen] = useState(false);

  const isLoggedIn = Boolean(account);
  const categories = [
    {
       code: "ai_ml_data_science",
       title: "AI, ML & Data Science",
       description: "Explore artificial intelligence, machine learning, deep learning, and data science.",
       icon: Brain,
       image: "/images/aiml.png",
    },
    {
       code: "computer_science",
       title: "Computer Science",
       description: "Build strong foundations in databases, operating systems, networks, and computer science.",
       icon: Network,
       image: "/images/cs.png",
    },
    {
      code: "programming",
      title: "Programming",
      description: "Develop programming skills through Python, Java, C++, and data structures.",
      icon: Code2,
      image: "/images/programing.png",
    },
  ];

  useEffect(() => {
    let active = true;

    const loadHomepage = async () => {
      const token = localStorage.getItem("token");

      if (!token) {
        try {
          const response = await api.get("/courses/");
          if (active) setCourses(response.data);
        } catch (error) {
          console.error("Unable to load public courses:", error);
        }
        return;
      }

      setLoading(true);

      try {
        const userResponse = await api.get("/users/me");

        if (!active) return;

        setAccount(userResponse.data);

        const [dashboardResult, coursesResult, enrollmentResult] =
          await Promise.allSettled([
            api.get("/dashboard/me"),
            api.get("/courses/"),
            api.get("/enrollments/me"),
          ]);

        if (!active) return;

        if (dashboardResult.status === "fulfilled") {
          setStats(dashboardResult.value.data);
        }

        if (coursesResult.status === "fulfilled") {
          setCourses(coursesResult.value.data);
        }

        if (
          coursesResult.status === "fulfilled" &&
          enrollmentResult.status === "fulfilled"
        ) {
          const enrolledIds = enrollmentResult.value.data.map(
            (enrollment) => enrollment.course_id
          );

          setMyCourses(
            coursesResult.value.data.filter((course) =>
              enrolledIds.includes(course.id)
            )
          );
        }
      } catch (error) {
        if (error.response?.status === 401) {
          localStorage.removeItem("token");
        }

        if (active) {
          setAccount(null);

          try {
            const response = await api.get("/courses/");
            if (active) setCourses(response.data);
          } catch (courseError) {
            console.error("Unable to load public courses:", courseError);
          }
        }
      } finally {
        if (active) setLoading(false);
      }
    };

    loadHomepage();

    return () => {
      active = false;
    };
  }, []);

  const firstName = account?.full_name?.trim().split(/\s+/)[0] || "Learner";

  return (
    <>
      <div className="home-page" data-theme={theme}>
        <nav className="home-navbar">
          <Link to="/" className="home-brand">
            <span className="home-brand-icon">
              <Brain size={23} />
            </span>
            <span>Learnova</span>
          </Link>

<div className={`home-nav-links ${menuOpen ? "menu-open" : ""}`}>
  <a href="#home" onClick={() => setMenuOpen(false)}>
    Home
  </a>

{isLoggedIn ? (
  <Link to="/courses" onClick={() => setMenuOpen(false)}>
    My Courses
  </Link>
) : (
  <a href="#courses" onClick={() => setMenuOpen(false)}>
    Courses
  </a>
)}

  <a href="#features" onClick={() => setMenuOpen(false)}>
    Features
  </a>

  <a href="#how-it-works" onClick={() => setMenuOpen(false)}>
    How It Works
  </a>
</div>


          <div className="home-nav-actions">
            <button
              className="home-theme-toggle"
              onClick={toggleTheme}
              aria-label="Toggle theme"
            >
              {theme === "dark" ? <Sun size={19} /> : <Moon size={19} />}
            </button>
                    {isLoggedIn ? (
                    <>
                    <Link to="/dashboard" className="home-login-button">
                    Dashboard
                    </Link>

                    <span className="home-user-greeting">
                    Hi, {firstName}
                    </span>

                    <button
                    className="home-signup-button"
                    onClick={handleLogout}
                    type="button"
                    >
                    Logout
                    </button>
                    </>
                    ) : (
              <>
                <Link to="/login" className="home-login-button">
                  Log In
                </Link>
                <Link to="/register" className="home-signup-button">
                  Get Started <ArrowRight size={16} />
                </Link>
              </>
            )}
          </div>

          <button
            className="home-mobile-menu"
            onClick={() => setMenuOpen((previous) => !previous)}
            aria-label="Toggle navigation"
          >
            {menuOpen ? <X /> : <Menu />}
          </button>
        </nav>

        <main>
          <section className="home-hero" id="home">
            <div className="home-hero-frame">
              <div className="home-window-controls">
                <span />
                <span />
                <span />
              </div>

              <div className="home-hero-grid">
                <div className="home-hero-content">
                  <div className="home-hero-badge">
                    <Brain size={15} />
                    AI-POWERED PERSONALIZED LEARNING
                  </div>

                  {isLoggedIn ? (
                    <>
                      <h1>
                        Welcome back,
                        <br />
                        <span>{firstName}.</span>
                      </h1>
                      <p className="home-hero-description">
                        Your learning journey continues here.
                        Explore your courses, track your progress,
                        and take the next step toward your goals.
                      </p>
                    </>
                  ) : (
                    <>
                      <h1>
                        A Personalized
                        <br />
                        Learning Experience
                        <br />
                        for <span>Every Learner</span>
                      </h1>
                      <p className="home-hero-description">
                        Learnova uses AI to understand your progress,
                        recommend the right learning materials, and
                        help you master each topic at your own pace.
                      </p>
                    </>
                  )}

                  <div className="home-hero-buttons">
                    {isLoggedIn ? (
                      <>
                        <Link to="/dashboard" className="home-primary-button">
                          Go to Dashboard <ArrowRight size={18} />
                        </Link>
                        <a href="#my-learning" className="home-secondary-button">
                          Continue Learning
                        </a>
                      </>
                    ) : (
                      <>
                        <Link to="/register" className="home-primary-button">
                          Get Started <ArrowRight size={18} />
                        </Link>
                        <a href="#courses" className="home-secondary-button">
                          <BookOpen size={18} /> Explore Courses
                        </a>
                      </>
                    )}
                  </div>
                </div>

                <div className="home-hero-art">
                  <div className="home-art-glow" />

                    <img
                    src={
                    theme === "light"
                    ? "/images/learnova-hero-light.png"
                    : "/images/learnova-hero.png"
                    }
                    alt="Learnova personalized learning visual"
                    className="home-spiral-image"
                    />

                </div>
              </div>

              <div className="home-hero-highlights">
                <div className="home-highlight">
                  <span className="home-highlight-icon">
                    <Target size={22} />
                  </span>
                  <div>
                    <strong>Personalized Paths</strong>
                    <p>Learn based on your goals</p>
                  </div>
                </div>

                <div className="home-highlight">
                  <span className="home-highlight-icon">
                    <ChartNoAxesCombined size={22} />
                  </span>
                  <div>
                    <strong>AI Recommendations</strong>
                    <p>Discover your next steps</p>
                  </div>
                </div>

                <div className="home-highlight">
                  <span className="home-highlight-icon">
                    <Layers3 size={22} />
                  </span>
                  <div>
                    <strong>Track Your Growth</strong>
                    <p>Understand your progress</p>
                  </div>
                </div>
              </div>
            </div>
          </section>

          {isLoggedIn && (
            <section className="home-personal-section" id="my-learning">
              <div className="home-section-heading">
                <span>YOUR LEARNING SPACE</span>
                <h2>Your learning at a glance</h2>
                <p>A snapshot of your progress so far.</p>
              </div>

              {loading ? (
                <p className="home-state">Loading your learning data...</p>
              ) : (
                <>
                  <div className="home-stats-grid">
                    {[
                      {
                        label: "Enrolled Courses",
                        value: stats?.enrolled_courses,
                        icon: BookOpen,
                      },
                      {
                        label: "Materials Completed",
                        value: stats?.learning_materials_completed,
                        icon: CheckCircle2,
                      },
                      {
                        label: "Quizzes Attempted",
                        value: stats?.quizzes_attempted,
                        icon: GraduationCap,
                      },
                      {
                        label: "Average Quiz Score",
                        value: stats?.average_quiz_percentage != null
                          ? `${stats.average_quiz_percentage}%`
                          : "—",
                        icon: Target,
                      },
                    ].map((item) => {
                      const Icon = item.icon;

                      return (
                        <article className="home-stat-card" key={item.label}>
                          <Icon size={22} />
                          <span>{item.label}</span>
                          <strong>{item.value ?? "—"}</strong>
                        </article>
                      );
                    })}
                  </div>

                  <div className="home-section-heading home-course-heading">
                    <span>CONTINUE LEARNING</span>
                    <h2>Your enrolled courses</h2>
                  </div>

                  {myCourses.length === 0 ? (
                    <div className="home-empty-state">
                      <BookOpen size={30} />
                      <h3>Your learning journey starts here</h3>
                      <p>You haven't enrolled in a course yet.</p>
                      <Link to="/courses" className="home-primary-button">
                        Explore Courses <ArrowRight size={17} />
                      </Link>
                    </div>
                  ) : (
                    
                    <div className="home-course-grid category-card-grid">
                    {categories.map((category) => {
                    const Icon = category.icon;

                    const courseCount = courses.filter(
                    (course) =>
                    course.category?.category_code === category.code
                    ).length;

                    return (
                    <Link
                    to={`/categories/${category.code}`}
                    className="home-course-card category-card"
                    key={category.code}
                    >
                    
                    <p style={{ color: "red" }}>
                    Image path: {category.image}
                    </p>
                    <div className="category-card-image">
                    <img
                    src={category.image}
                    alt={category.title}
                    />
                    <div className="category-image-overlay" />
                    <div className="category-card-icon">
                    <Icon size={23} />
                    </div>
                    </div>

                    <div className="category-card-content">
                    <span className="category-card-label">
                    LEARNING CATEGORY
                    </span>

                    <h3>{category.title}</h3>

                    <p>{category.description}</p>

                    <div className="category-card-footer">
                    <span>{courseCount} Courses Available</span>
                    <span className="category-explore">
                    Explore Category
                    <ArrowRight size={17} />
                    </span>
                    </div>
                    </div>
                    </Link>
                    );
                    })}
                    </div>

                  )}

                  <Link to="/dashboard" className="home-dashboard-link">
                    View Full Dashboard <ArrowRight size={17} />
                  </Link>
                </>
              )}
            </section>
          )}

         
                    {!isLoggedIn && (
                    <section className="home-courses-section" id="courses">
                    <div className="home-section-heading">
                    <span>EXPLORE AND DISCOVER</span>
                    <h2>Find Your Learning Path</h2>
                    <p>
                    Choose your learning domain and explore courses designed
                    to help you grow.
                    </p>
                    </div>

                    <div className="home-course-grid category-card-grid">
                    {categories.map((category) => {
                    const Icon = category.icon;

                    const courseCount = courses.filter(
                    (course) =>
                    course.category?.category_code === category.code
                    ).length;

                    return (
                    <Link
                    to={`/categories/${category.code}`}
                    className="home-course-card category-card"
                    key={category.code}
                    >
                    <div className="category-card-image">
                    <img
                    src={category.image}
                    alt={category.title}
                    />

                    <div className="category-image-overlay" />

                    <div className="category-card-icon">
                    <Icon size={23} />
                    </div>
                    </div>

                    <div className="category-card-content">
                    <span className="category-card-label">
                    LEARNING CATEGORY
                    </span>

                    <h3>{category.title}</h3>

                    <p>{category.description}</p>

                    <div className="category-card-footer">
                    <span>{courseCount} Courses Available</span>

                    <span className="category-explore">
                    Explore Category
                    <ArrowRight size={17} />
                    </span>
                    </div>
                    </div>
                    </Link>
                    );
                    })}
                    </div>
                    </section>
                    )}


          <section className="home-features-section" id="features">
            <div className="home-section-heading">
              <span>WHY LEARNOVA</span>
              <h2>Learning built around you</h2>
              <p>Tools that make your learning journey more focused and meaningful.</p>
            </div>

            <div className="home-feature-grid">
              <article className="home-feature-card">
                <Brain size={25} />
                <h3>Personalized Learning</h3>
                <p>Learning recommendations aligned with your goals and interests.</p>
              </article>

              <article className="home-feature-card">
                <ChartNoAxesCombined size={25} />
                <h3>Track Your Progress</h3>
                <p>Monitor topic mastery and understand your learning growth.</p>
              </article>

              <article className="home-feature-card">
                <BookOpen size={25} />
                <h3>Learn at Your Pace</h3>
                <p>Explore courses, materials, and quizzes at your own pace.</p>
              </article>
            </div>
          </section>

          <section className="home-how-section" id="how-it-works">
            <div className="home-section-heading">
              <span>YOUR JOURNEY</span>
              <h2>A simpler way to move forward</h2>
            </div>

            <div className="home-steps-grid">
              <article><strong>01</strong><h3>Set Your Goals</h3><p>Tell Learnova what you want to achieve.</p></article>
              <article><strong>02</strong><h3>Learn Your Way</h3><p>Explore courses and learning materials.</p></article>
              <article><strong>03</strong><h3>Track Your Growth</h3><p>Review your progress and improve over time.</p></article>
            </div>
          </section>
        </main>

        <footer className="home-footer">
          <Link to="/" className="home-brand">
            <span className="home-brand-icon"><Brain size={21} /></span>
            Learnova
          </Link>
          <p>Your goals. Your pace. Your learning journey.</p>
        </footer>
      </div>

      {showIntro && (
        <LearnovaIntro onComplete={onIntroComplete} />
      )}
    </>
  );
}

export default Home;
