
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../services/api";
import DashboardLayout from "../components/DashboardLayout";
import "./Quizzes.css";

function Quizzes() {
  const [quizzes, setQuizzes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    const fetchQuizzes = async () => {
      try {
        const enrollmentResponse = await api.get("/enrollments/me");
        const coursesResponse = await api.get("/courses/");

        const enrolledCourseIds =
          enrollmentResponse.data.map(
            (enrollment) => enrollment.course_id
          );

        const enrolledCourses =
          coursesResponse.data.filter((course) =>
            enrolledCourseIds.includes(course.id)
          );

        const courseTopics = await Promise.all(
          enrolledCourses.map(async (course) => {
            const response = await api.get(
              `/dashboard/course/${course.id}/topics`
            );

            return response.data;
          })
        );

        const topics = courseTopics.flat();

        const topicQuizzes = await Promise.all(
          topics.map(async (topic) => {
            const response = await api.get(
              `/quizzes/topic/${topic.topic_id}`
            );

            return response.data.map((quiz) => ({
              ...quiz,
              topicTitle: topic.topic_title,
            }));
          })
        );

        setQuizzes(topicQuizzes.flat());
      } catch (err) {
        setError(
          err.response?.data?.detail ||
            "Unable to load quizzes"
        );
      } finally {
        setLoading(false);
      }
    };

    fetchQuizzes();
  }, []);

  return (
    <DashboardLayout
      title="Quizzes"
      subtitle="Test your understanding and track your learning."
    >
      {loading && <p>Loading quizzes...</p>}

      {error && <p className="dashboard-error">{error}</p>}

      {!loading && !error && quizzes.length === 0 && (
        <div className="quiz-empty">
          <h2>No quizzes available</h2>
          <p>Quizzes for your enrolled courses will appear here.</p>
        </div>
      )}

      <div className="quiz-grid">
        {quizzes.map((quiz) => (
          <article className="quiz-card" key={quiz.id}>
            <div className="quiz-card-icon">📝</div>

            <h2>{quiz.title}</h2>

            <p className="quiz-topic">{quiz.topicTitle}</p>

            <p className="quiz-description">
              {quiz.description || "Test your knowledge of this topic."}
            </p>

            <button
              className="quiz-start-button"
              onClick={() => navigate(`/quizzes/${quiz.id}/attempt`)}
            >
              Start Quiz
            </button>
          </article>
        ))}
      </div>
    </DashboardLayout>
  );
}

export default Quizzes;
