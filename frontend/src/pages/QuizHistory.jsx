import { useEffect, useState } from "react";
import api from "../services/api";
import DashboardLayout from "../components/DashboardLayout";
import "./QuizHistory.css";

function QuizHistory() {
  const [attempts, setAttempts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchAttempts = async () => {
      try {
        const response = await api.get("/quiz-attempts/me");
        setAttempts(response.data);
      } catch (err) {
        setError(
          err.response?.data?.detail ||
            "Unable to load quiz history"
        );
      } finally {
        setLoading(false);
      }
    };

    fetchAttempts();
  }, []);

  return (
    <DashboardLayout
      title="Quiz History"
      subtitle="Review your previous quiz attempts and scores."
    >
      <section className="quiz-history-section">
        {loading && <p>Loading quiz history...</p>}

        {error && <p className="error-message">{error}</p>}

        {!loading && !error && attempts.length === 0 && (
          <div className="empty-history">
            <h3>No quiz attempts yet</h3>
            <p>Complete a quiz to see your results here.</p>
          </div>
        )}

        {!loading && attempts.length > 0 && (
          <div className="quiz-history-list">
            {attempts.map((attempt) => {
              const percentage =
                attempt.total_questions > 0
                  ? (
                      (attempt.score /
                        attempt.total_questions) *
                      100
                    ).toFixed(2)
                  : 0;

              return (
                <div
                  className="quiz-history-card"
                  key={attempt.id}
                >
                  <div>
                    <h3>Quiz #{attempt.quiz_id}</h3>
                    <p>
                      Attempt ID: {attempt.id}
                    </p>
                    <p>
                      Submitted:{" "}
                      {attempt.submitted_at
                        ? new Date(
                            attempt.submitted_at
                          ).toLocaleString()
                        : "Not submitted"}
                    </p>
                  </div>

                  <div className="quiz-history-score">
                    <h2>
                      {attempt.score}/
                      {attempt.total_questions}
                    </h2>
                    <span>{percentage}%</span>
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </section>
    </DashboardLayout>
  );
}

export default QuizHistory;
