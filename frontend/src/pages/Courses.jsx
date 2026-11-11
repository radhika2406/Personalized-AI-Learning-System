
import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import {
  BookOpen,
  GraduationCap,
  ArrowRight,
  CheckCircle2,
  Code2,
  LoaderCircle,
} from "lucide-react";

import api from "../services/api";
import DashboardLayout from "../components/DashboardLayout";
import "./Courses.css";

function Courses() {
  const [courses, setCourses] = useState([]);
  const [enrolledCourseIds, setEnrolledCourseIds] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [enrollingId, setEnrollingId] = useState(null);

  useEffect(() => {
    let isMounted = true;

    const fetchCourses = async () => {
      try {
        const [coursesResponse, enrollmentResponse] =
          await Promise.all([
            api.get("/courses/"),
            api.get("/enrollments/me"),
          ]);

        if (!isMounted) return;

        setCourses(coursesResponse.data);
        setEnrolledCourseIds(
          enrollmentResponse.data.map(
            (enrollment) => enrollment.course_id
          )
        );
      } catch (err) {
        if (!isMounted) return;

        setError(
          err.response?.data?.detail ||
            "Unable to load courses. Please try again."
        );
      } finally {
        if (isMounted) setLoading(false);
      }
    };

    fetchCourses();

    return () => {
      isMounted = false;
    };
  }, []);

  const handleEnroll = async (courseId) => {
    setEnrollingId(courseId);
    setError("");

    try {
      await api.post(`/enrollments/courses/${courseId}`);

      setEnrolledCourseIds((previousIds) =>
        previousIds.includes(courseId)
          ? previousIds
          : [...previousIds, courseId]
      );
    } catch (err) {
      setError(
        err.response?.data?.detail ||
          "Enrollment failed. Please try again."
      );
    } finally {
      setEnrollingId(null);
    }
  };

  const enrolledCount = enrolledCourseIds.length;

  return (
    <DashboardLayout
      title="My Courses"
      subtitle="Explore courses and build your learning journey."
    >
      <main className="courses-page">

        <section className="courses-hero">
          <div className="courses-hero-content">
            <span className="courses-eyebrow">
              <GraduationCap size={15} />
              YOUR LEARNING LIBRARY
            </span>

            <h2>Discover your next learning experience.</h2>

            <p>
              Explore available courses, enroll in the ones
              that interest you, and keep moving forward.
            </p>
          </div>

          <div className="courses-hero-icon">
            <BookOpen size={58} strokeWidth={1.5} />
          </div>
        </section>

        <section className="courses-overview">
          <div className="courses-section-heading">
            <div>
              <span className="courses-section-eyebrow">
                COURSE CATALOG
              </span>
              <h2>Explore Courses</h2>
              <p>Find the right course for your learning goals.</p>
            </div>

            {!loading && !error && (
              <div className="courses-count">
                <BookOpen size={17} />
                <span>{courses.length} Available</span>
              </div>
            )}
          </div>

          {!loading && !error && courses.length > 0 && (
            <div className="courses-summary">
              <div className="courses-summary-item">
                <span>Total Courses</span>
                <strong>{courses.length}</strong>
              </div>

              <div className="courses-summary-item">
                <span>Enrolled Courses</span>
                <strong>{enrolledCount}</strong>
              </div>
            </div>
          )}

          {loading && (
            <div className="courses-state">
              <LoaderCircle className="courses-spinner" size={34} />
              <h3>Loading your courses</h3>
              <p>Getting the available courses ready for you.</p>
            </div>
          )}

          {error && (
            <div className="courses-error" role="alert">
              <p>{error}</p>
            </div>
          )}

          {!loading && !error && courses.length === 0 && (
            <div className="courses-state">
              <div className="courses-empty-icon">
                <BookOpen size={30} />
              </div>
              <h3>No courses available yet</h3>
              <p>
                New courses will appear here when they become available.
              </p>
            </div>
          )}

          {!loading && courses.length > 0 && (
            <div className="courses-grid">
              {courses.map((course) => {
                const isEnrolled = enrolledCourseIds.includes(course.id);
                const isEnrolling = enrollingId === course.id;

                return (
                  <article className="catalog-course-card" key={course.id}>
                    <div className="catalog-card-top">
                      <div className="catalog-course-icon">
                        <Code2 size={25} />
                      </div>

                      {isEnrolled && (
                        <span className="enrolled-badge">
                          <CheckCircle2 size={14} />
                          Enrolled
                        </span>
                      )}
                    </div>

                    <div className="catalog-course-content">
                      <span className="catalog-course-code">
                        {course.course_code || "COURSE"}
                      </span>

                      <h3>
                        <Link to={`/courses/${course.id}`}>
                          {course.title}
                        </Link>
                      </h3>

                      <p>
                        {course.description ||
                          "No description available for this course."}
                      </p>
                    </div>

                    <div className="catalog-course-actions">
                      <Link
                        to={`/courses/${course.id}`}
                        className="course-details-link"
                      >
                        View Details
                        <ArrowRight size={16} />
                      </Link>

                      <button
                        type="button"
                        className={`course-enroll-button ${
                          isEnrolled ? "is-enrolled" : ""
                        }`}
                        disabled={isEnrolled || isEnrolling}
                        onClick={() => handleEnroll(course.id)}
                      >
                        {isEnrolling ? (
                          <>
                            <LoaderCircle size={16} className="courses-spinner" />
                            Enrolling...
                          </>
                        ) : isEnrolled ? (
                          <>
                            <CheckCircle2 size={16} />
                            Enrolled
                          </>
                        ) : (
                          "Enroll Now"
                        )}
                      </button>
                    </div>
                  </article>
                );
              })}
            </div>
          )}
        </section>
      </main>
    </DashboardLayout>
  );
}

export default Courses;
