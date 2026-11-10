import { ArrowRight, BookOpen, Brain, ChartNoAxesCombined } from "lucide-react";
import { BrowserRouter, Routes, Route, Link } from "react-router-dom";
import React, { useState } from "react";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Dashboard from "./dashboard.jsx";
import Courses from "./pages/Courses";
import CourseDetails from "./pages/CourseDetails";
import LearningMaterials from "./pages/LearningMaterials";
import Quizzes from "./pages/Quizzes";
import QuizAttempt from "./pages/QuizAttempt";
import QuizHistory from "./pages/QuizHistory";
import Recommendations from "./pages/Recommendations";
import Profile from "./pages/Profile";
import LearningPath from "./pages/LearningPath";
import "./App.css";

function Home() {
  const [theme, setTheme] = useState(() => {
      return localStorage.getItem("learnova-theme") || "dark";
    });
    const toggleTheme = () => {
      const newTheme = theme === "dark" ? "light" : "dark";

      setTheme(newTheme);
      localStorage.setItem("learnova-theme", newTheme);
    };
    return (
    <div
      className="landing-page"
      data-theme={theme}
    >
      <nav className="navbar">
        <div className="brand">
          <div className="brand-icon">
            <Brain size={22} />
          </div>
          <span>Learnova</span>
        </div>

        <div className="nav-links">
          <a href="#features">Features</a>
          <a href="#about">About</a>
        </div>

        <div className="nav-actions">
          <button
            className="theme-toggle"
            onClick={toggleTheme}
            aria-label="Toggle theme"
            title={theme === "dark" ? "Switch to Light Theme" : "Switch to Dark Theme"}
          >
            {theme === "dark" ? "☀️" : "🌙"}
          </button>
          <Link to="/login" className="login-btn">Log in</Link>
          <Link to="/register" className="signup-btn">
            Get Started <ArrowRight size={16} />
          </Link>
        </div>
      </nav>

      <main>
        <section className="hero">
          <div className="hero-content">
            <div className="hero-badge">
              <Brain size={15} />
              Personalized learning, reimagined
            </div>

            <h1>
              Learning that
              <br />
              <span>adapts to you.</span>
            </h1>

            <p className="hero-description">
              Discover a smarter way to learn. Explore courses,
              track your progress, and grow at your own pace
              with a learning experience built around you.
            </p>

            <div className="hero-actions">
              <Link to="/register" className="primary-button">
                Start Learning <ArrowRight size={18} />
              </Link>

              <a href="#features" className="secondary-button">
                Explore Features
              </a>
            </div>

            <div className="hero-note">
              Your goals. Your pace. Your learning journey.
            </div>
          </div>

          <div className="hero-preview">
            <div className="preview-header">
              <div>
                <p className="preview-label">YOUR LEARNING OVERVIEW</p>
                <h3>Welcome back, learner 👋</h3>
              </div>
              <div className="preview-avatar">L</div>
            </div>

            <div className="preview-stats">
              <div className="stat-card">
                <BookOpen size={20} />
                <p>Courses</p>
                <h2>04</h2>
              </div>

              <div className="stat-card">
                <ChartNoAxesCombined size={20} />
                <p>Progress</p>
                <h2>72%</h2>
              </div>
            </div>

            <div className="progress-section">
              <div className="progress-heading">
                <span>Learning progress</span>
                <span>72%</span>
              </div>
              <div className="progress-track">
                <div className="progress-fill" />
              </div>
            </div>

            <div className="preview-course">
              <div className="course-icon">
                <Brain size={20} />
              </div>
              <div>
                <h4>Introduction to AI</h4>
                <p>Continue your learning journey</p>
              </div>
              <ArrowRight size={18} />
            </div>
          </div>
        </section>

        <section className="features-section" id="features">
          <div className="section-heading">
            <p className="section-label">A BETTER WAY TO LEARN</p>
            <h2>Learning built around you</h2>
            <p>
              Everything you need to make your learning journey
              more focused, meaningful, and effective.
            </p>
          </div>

          <div className="features-grid">
            <article className="feature-card">
              <div className="feature-icon"><Brain size={22} /></div>
              <h3>Personalized Learning</h3>
              <p>Learning recommendations that align with your goals, progress, and interests.</p>
            </article>

            <article className="feature-card">
              <div className="feature-icon"><ChartNoAxesCombined size={22} /></div>
              <h3>Track Your Progress</h3>
              <p>Understand your growth, monitor topic mastery, and celebrate your learning milestones.</p>
            </article>

            <article className="feature-card">
              <div className="feature-icon"><BookOpen size={22} /></div>
              <h3>Learn at Your Pace</h3>
              <p>Explore structured courses, learning materials, and quizzes at your own pace.</p>
            </article>
          </div>
        </section>
      </main>

      <footer className="footer" id="about">
        <p>Learnova — Your personal learning journey.</p>
      </footer>
    </div>
  );
}

function LoginPlaceholder() {
  return (
    <div className="auth-container">
      <div className="auth-card">
        <h1>Login</h1>
        <p>Login page will be implemented next.</p>
        <Link to="/register">Create an account</Link>
        <br />
        <Link to="/">Back to Home</Link>
      </div>
    </div>
  );
}

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/register" element={<Register />} />
        <Route path="/login" element={<Login />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/courses" element={<Courses />} />
        <Route path="/materials" element={<LearningMaterials />} />
        <Route
          path="/courses/:courseId"
          element={<CourseDetails />}
        />
        <Route
          path="/topics/:topicId/materials"
          element={<LearningMaterials />}
        />
        <Route path="/quizzes" element={<Quizzes />} />
        <Route
        path="/quizzes/:quizId/attempt"
        element={<QuizAttempt />}
        />
        <Route
          path="/quiz-history"
          element={<QuizHistory />}
        />
        <Route
          path="/recommendations"
          element={<Recommendations />}
        />
        <Route path="/profile" element={<Profile />} />
        <Route path="/learning-path" element={<LearningPath />} />
        </Routes>
        </BrowserRouter>
  );
}

export default App;
