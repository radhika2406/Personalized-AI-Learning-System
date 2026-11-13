
import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import {
  ArrowLeft,
  ArrowRight,
  BookOpen,
  BrainCircuit,
  Code2,
  Network,
  LoaderCircle,
  Sun,
  Moon,
} from "lucide-react";

import api from "../services/api";
import DashboardLayout from "../components/DashboardLayout";
import Logo from "../components/Logo";
import { useTheme } from "../ThemeContext";
import "./CategoryCourses.css";

const categoryConfig = {
  ai_ml_data_science: {
    title: "AI, ML & Data Science",
    description:
      "Explore artificial intelligence, machine learning, deep learning, and data science.",
    icon: BrainCircuit,
  },
  computer_science: {
    title: "Computer Science",
    description:
      "Build strong foundations in databases, operating systems, networks, and software concepts.",
    icon: Network,
  },
  programming: {
    title: "Programming",
    description:
      "Develop programming skills through Python, Java, C++, and data structures and algorithms.",
    icon: Code2,
  },
};

function CategoryCourses() {
  const { categoryCode } = useParams();
  const { theme, toggleTheme } = useTheme();

  const [courses, setCourses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const isLoggedIn = Boolean(localStorage.getItem("token"));
  const category = categoryConfig[categoryCode];
  const CategoryIcon = category?.icon || BookOpen;

  useEffect(() => {
    let active = true;

    const fetchCourses = async () => {
      setLoading(true);
      setError("");

      try {
        const response = await api.get("/courses/");

        if (!active) return;

        setCourses(
          response.data.filter(
            (course) =>
              course.category?.category_code === categoryCode
          )
        );
      } catch (err) {
        if (active) {
          setError(
            err.response?.data?.detail ||
              "Unable to load courses. Please try again."
          );
        }
      } finally {
        if (active) setLoading(false);
      }
    };

    if (category) {
      fetchCourses();
    } else {
      setLoading(false);
      setError("The requested category was not found.");
    }

    return () => {
      active = false;
    };
  }, [categoryCode, category]);

  const pageContent = (
    <main className="category-courses-page">
      <Link
        to="/"
        className="category-back-link"
      >
        <ArrowLeft size={17} />
        Back to Home
      </Link>

      <section className="category-hero">
        <div className="category-hero-content">
          <span className="category-eyebrow">
            <BookOpen size={15} />
            LEARNOVA LEARNING DOMAIN
          </span>

          <h2>{category?.title || "Learning Category"}</h2>

          <p>
            {category?.description ||
              "Explore available learning opportunities."}
          </p>
        </div>

        <div className="category-hero-icon">
          <CategoryIcon size={55} strokeWidth={1.5} />
        </div>
      </section>

      <section className="category-course-section">
        <div className="category-section-heading">
          <div>
            <span>AVAILABLE COURSES</span>
            <h2>Explore Your Courses</h2>
            <p>Choose a course to begin your learning journey.</p>
          </div>

          {!loading && !error && (
            <div className="category-course-count">
              <BookOpen size={17} />
              {courses.length} Courses
            </div>
          )}
        </div>

        {loading && (
          <div className="category-state">
            <LoaderCircle
              className="category-spinner"
              size={34}
            />
            <h3>Loading courses...</h3>
          </div>
        )}

        {error && (
          <div className="category-error" role="alert">
            {error}
          </div>
        )}

        {!loading && !error && courses.length === 0 && (
          <div className="category-state">
            <BookOpen size={30} />
            <h3>No courses available</h3>
            <p>Courses will appear here when available.</p>
          </div>
        )}

        {!loading && !error && courses.length > 0 && (
          <div className="category-course-grid">
            {courses.map((course) => (
              <article
                className="category-course-card"
                key={course.id}
              >
                <div className="category-course-icon">
                  <CategoryIcon size={24} />
                </div>

                <span>
                  {course.course_code || "COURSE"}
                </span>

                <h3>{course.title}</h3>

                <p>
                  {course.description ||
                    "Explore topics and develop your knowledge."}
                </p>

                <Link to={`/courses/${course.id}`}>
                  Explore Course
                  <ArrowRight size={16} />
                </Link>
              </article>
            ))}
          </div>
        )}
      </section>
    </main>
  );

  if (isLoggedIn) {
    return (
      <DashboardLayout
        title={category?.title || "Category"}
        subtitle="Explore courses in your chosen learning domain."
      >
        {pageContent}
      </DashboardLayout>
    );
  }

  return (
    <div
      className="public-category-layout"
      data-theme={theme}
    >
      <header className="public-category-header">
        <Link to="/" className="public-category-brand">
          <Logo />
        </Link>

        <div className="public-category-header-actions">
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

          <Link to="/login" className="public-category-login">
            Log In
          </Link>

          <Link
            to="/register"
            className="public-category-register"
          >
            Get Started
          </Link>
        </div>
      </header>

      <div className="public-category-content">
        {pageContent}
      </div>
    </div>
  );
}

export default CategoryCourses;
