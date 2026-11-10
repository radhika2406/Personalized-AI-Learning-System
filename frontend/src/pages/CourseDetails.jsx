import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { useNavigate } from "react-router-dom";
import api from "../services/api";

function CourseDetails() {
  const { courseId } = useParams();
  const navigate = useNavigate();
  const [course, setCourse] = useState(null);
  const [topics, setTopics] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchCourseDetails = async () => {
      try {
        const [courseResponse, topicsResponse] =
          await Promise.all([
            api.get(`/courses/${courseId}`),
            api.get(`/dashboard/course/${courseId}/topics`),
          ]);

        setCourse(courseResponse.data);
        setTopics(topicsResponse.data);
      } catch (err) {
        setError(
          err.response?.data?.detail ||
            "Unable to load course details"
        );
      } finally {
        setLoading(false);
      }
    };

    fetchCourseDetails();
  }, [courseId]);

  if (loading) {
    return <p>Loading course details...</p>;
  }

  if (error) {
    return <p>{error}</p>;
  }

  return (
    <div>
      <h1>{course.title}</h1>
      <p>Course Code: {course.course_code}</p>
      <p>{course.description || "No description available."}</p>

      <h2>Course Topics</h2>

      {topics.length === 0 ? (
        <p>No topics available for this course yet.</p>
      ) : (
        topics.map((topic) => (
          <div key={topic.topic_id}>
            <h3
                    onClick={() =>
                    navigate(`/topics/${topic.topic_id}/materials`)
                    }
                    style={{ cursor: "pointer" }}
                    >
                    {topic.sequence_number}. {topic.topic_title}
                    </h3>
            <p>
              Learning Materials:{" "}
              {topic.completed_learning_materials}/
              {topic.total_learning_materials} completed
            </p>
            <p>Mastery: {topic.mastery_score}%</p>
          </div>
        ))
      )}
    </div>
  );
}

export default CourseDetails;
