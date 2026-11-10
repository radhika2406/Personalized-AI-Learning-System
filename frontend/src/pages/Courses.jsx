import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../services/api";

function Courses() {
  const navigate = useNavigate();                  
  const [courses, setCourses] = useState([]);
  const [enrolledCourseIds, setEnrolledCourseIds] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [enrollingId, setEnrollingId] = useState(null);

  useEffect(() => {
    const fetchCourses = async () => {
      try {
        const [coursesResponse, enrollmentResponse] =
          await Promise.all([
            api.get("/courses/"),
            api.get("/enrollments/me"),
          ]);

        setCourses(coursesResponse.data);

        setEnrolledCourseIds(
          enrollmentResponse.data.map(
            (enrollment) => enrollment.course_id
          )
        );
      } catch (err) {
        setError(
          err.response?.data?.detail ||
            "Unable to load courses"
        );
      } finally {
        setLoading(false);
      }
    };

    fetchCourses();
  }, []);

  const handleEnroll = async (courseId) => {
    setEnrollingId(courseId);
    setError("");

    try {
      await api.post(`/enrollments/courses/${courseId}`);

      setEnrolledCourseIds((previousIds) => [
        ...previousIds,
        courseId,
      ]);
    } catch (err) {
      setError(
        err.response?.data?.detail ||
          "Enrollment failed"
      );
    } finally {
      setEnrollingId(null);
    }
  };

  if (loading) {
    return <div>Loading courses...</div>;
  }

  if (error && courses.length === 0) {
    return <div>{error}</div>;
  }

  return (
    <div>
      <h1>Course Catalog</h1>
      <p>Explore available courses and start learning.</p>

      {error && <p>{error}</p>}

      {courses.length === 0 ? (
        <p>No courses are available yet.</p>
      ) : (
        <div>
          {courses.map((course) => {
            const isEnrolled =
              enrolledCourseIds.includes(course.id);

            return (
              <div key={course.id}>
               <h3
                    onClick={() => navigate(`/courses/${course.id}`)}
                    style={{ cursor: "pointer" }}
                    >
                    {course.title}
                    </h3>
                <p>Course Code: {course.course_code}</p>
                <p>
                  {course.description ||
                    "No description available."}
                </p>

                <button
                  disabled={
                    isEnrolled ||
                    enrollingId === course.id
                  }
                  onClick={() => handleEnroll(course.id)}
                >
                  {isEnrolled
                    ? "Enrolled"
                    : enrollingId === course.id
                    ? "Enrolling..."
                    : "Enroll"}
                </button>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}

export default Courses;
