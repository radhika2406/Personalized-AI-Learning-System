
import { useEffect, useState } from "react";
import api from "../services/api";
import DashboardLayout from "../components/DashboardLayout";
import "./QuizHistory.css";

function QuizHistory() {
  const [attempts, setAttempts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [expandedAttempt, setExpandedAttempt] = useState(null);
  const [reviews, setReviews] = useState({});
  const [reviewLoading, setReviewLoading] = useState({});
  const [reviewErrors, setReviewErrors] = useState({});

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

  const handleReview = async (attemptId) => {
    if (expandedAttempt === attemptId) {
      setExpandedAttempt(null);
      return;
    }

    setExpandedAttempt(attemptId);

    if (reviews[attemptId]) {
      return;
    }

    setReviewLoading((previous) => ({
      ...previous,
      [attemptId]: true,
    }));

    setReviewErrors((previous) => ({
      ...previous,
      [attemptId]: "",
    }));

    try {
      const response = await api.get(
        `/quiz-attempts/${attemptId}/review`
      );

      setReviews((previous) => ({
        ...previous,
        [attemptId]: response.data,
      }));
    } catch (err) {
      setReviewErrors((previous) => ({
        ...previous,
        [attemptId]:
          err.response?.data?.detail ||
          "Unable to load answer review",
      }));
    } finally {
      setReviewLoading((previous) => ({
        ...previous,
        [attemptId]: false,
      }));
    }
  };

  const getOptionText = (question, option) => {
    const optionMap = {
      A: question.option_a,
      B: question.option_b,
      C: question.option_c,
      D: question.option_d,
    };

    return optionMap[option] || "Not available";
  };

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

        {!loading && !error && attempts.length > 0 && (
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

              const isExpanded =
                expandedAttempt === attempt.id;

              const review = reviews[attempt.id];

              return (
                <div key={attempt.id}>
                  <div className="quiz-history-card">
                    <div className="quiz-history-info">
                      <h3>Quiz #{attempt.quiz_id}</h3>

                      <p>Attempt ID: {attempt.id}</p>

                      <p>
                        Submitted:{" "}
                        {attempt.submitted_at
                          ? new Date(
                              attempt.submitted_at
                            ).toLocaleString()
                          : "Not submitted"}
                      </p>

                      <button
                        className="quiz-history-review-button"
                        onClick={() =>
                          handleReview(attempt.id)
                        }
                      >
                        {isExpanded
                          ? "Hide Review ↑"
                          : "Review Answers →"}
                      </button>
                    </div>

                    <div className="quiz-history-score">
                      <h2>
                        {attempt.score}/
                        {attempt.total_questions}
                      </h2>

                      <span>{percentage}%</span>
                    </div>
                  </div>

                  {isExpanded && (
                    <div className="history-review-panel">
                      {reviewLoading[attempt.id] && (
                        <p>Loading answer review...</p>
                      )}

                      {reviewErrors[attempt.id] && (
                        <p className="error-message">
                          {reviewErrors[attempt.id]}
                        </p>
                      )}

                      {review && (
                        <>
                          <div className="history-review-heading">
                            <h3>Answer Review</h3>
                            <span>
                              {review.review.length} Questions
                            </span>
                          </div>

                          <div className="history-review-list">
                            {review.review.map(
                              (item, index) => (
                                <article
                                  className={`history-review-card ${
                                    item.is_correct
                                      ? "review-correct"
                                      : "review-incorrect"
                                  }`}
                                  key={item.question_id}
                                >
                                  <div className="history-review-card-header">
                                    <span>
                                      Question {index + 1}
                                    </span>

                                    <span
                                      className={
                                        item.is_correct
                                          ? "history-status-correct"
                                          : "history-status-incorrect"
                                      }
                                    >
                                      {item.is_correct
                                        ? "✓ Correct"
                                        : "✕ Incorrect"}
                                    </span>
                                  </div>

                                  <h4>{item.question_text}</h4>

                                  <div className="history-review-options">
                                    {["A", "B", "C", "D"].map(
                                      (option) => {
                                        const isSelected =
                                          item.selected_option ===
                                          option;

                                        const isCorrect =
                                          item.correct_option ===
                                          option;

                                        return (
                                          <div
                                            key={option}
                                            className={`history-review-option ${
                                              isCorrect
                                                ? "correct-answer"
                                                : isSelected
                                                  ? "wrong-answer"
                                                  : ""
                                            }`}
                                          >
                                            <strong>
                                              {option}
                                            </strong>

                                            <span>
                                              {getOptionText(
                                                item,
                                                option
                                              )}
                                            </span>

                                            <small>
                                              {isCorrect
                                                ? "Correct answer"
                                                : isSelected
                                                  ? "Your answer"
                                                  : ""}
                                            </small>
                                          </div>
                                        );
                                      }
                                    )}
                                  </div>

                                  <div className="history-review-explanation">
                                    <strong>Explanation</strong>
                                    <p>
                                      {item.explanation ||
                                        "No explanation is available for this question."}
                                    </p>
                                  </div>
                                </article>
                              )
                            )}
                          </div>
                        </>
                      )}
                    </div>
                  )}
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
