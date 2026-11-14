
import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import api from "../services/api";
import DashboardLayout from "../components/DashboardLayout";
import "./QuizAttempt.css";

function QuizAttempt() {
  const { quizId } = useParams();
  const navigate = useNavigate();

  const [quiz, setQuiz] = useState(null);
  const [questions, setQuestions] = useState([]);
  const [answers, setAnswers] = useState({});
  const [currentIndex, setCurrentIndex] = useState(0);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchQuiz = async () => {
      try {
        const [quizResponse, questionsResponse] =
          await Promise.all([
            api.get(`/quizzes/${quizId}`),
            api.get(`/quizzes/${quizId}/questions`),
          ]);

        setQuiz(quizResponse.data);
        setQuestions(questionsResponse.data);
      } catch (err) {
        setError(
          err.response?.data?.detail ||
            "Unable to load quiz"
        );
      } finally {
        setLoading(false);
      }
    };

    fetchQuiz();
  }, [quizId]);

  const selectAnswer = (questionId, option) => {
    setAnswers((previous) => ({
      ...previous,
      [questionId]: option,
    }));
  };

  const handleSubmit = async () => {
    if (Object.keys(answers).length !== questions.length) {
      setError("Please answer every question before submitting.");
      return;
    }

    setSubmitting(true);
    setError("");

    try {
      const submission = {
        answers: questions.map((question) => ({
          question_id: question.id,
          selected_option: answers[question.id],
        })),
      };

      const response = await api.post(
        `/quiz-attempts/quiz/${quizId}/submit`,
        submission
      );

      setResult(response.data);
    } catch (err) {
      setError(
        err.response?.data?.detail ||
          "Unable to submit quiz"
      );
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) {
    return (
      <DashboardLayout
        title="Quiz"
        subtitle="Loading your quiz..."
      >
        <p>Loading questions...</p>
      </DashboardLayout>
    );
  }

  if (error && !quiz) {
    return (
      <DashboardLayout title="Quiz" subtitle="">
        <p>{error}</p>
      </DashboardLayout>
    );
  }

  if (result) {
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
        title="Quiz Result"
        subtitle="Your quiz has been submitted successfully."
      >
        <div className="quiz-result-card">
          <div className="quiz-result-icon">🎉</div>

          <h2>{quiz.title}</h2>

          <div className="quiz-result-score">
            {result.percentage}%
          </div>

          <p>
            You scored {result.score} out of{" "}
            {result.total_questions}
          </p>

          <div className="quiz-result-progress">
            <div
              style={{
                width: `${result.percentage}%`,
              }}
            />
          </div>

          <button
            className="quiz-start-button"
            onClick={() => navigate("/quizzes")}
          >
            Back to Quizzes
          </button>
        </div>

        <section className="quiz-review-section">
          <div className="quiz-review-heading">
            <div>
              <h2>Answer Review</h2>
              <p>
                Review your answers and understand the correct
                solutions.
              </p>
            </div>

            <span className="quiz-review-count">
              {result.review?.length || 0} Questions
            </span>
          </div>

          {result.review?.length > 0 ? (
            <div className="quiz-review-list">
              {result.review.map((item, index) => (
                <article
                  className={`quiz-review-card ${
                    item.is_correct
                      ? "review-correct"
                      : "review-incorrect"
                  }`}
                  key={item.question_id}
                >
                  <div className="quiz-review-card-header">
                    <span className="quiz-review-number">
                      Question {index + 1}
                    </span>

                    <span
                      className={`quiz-review-status ${
                        item.is_correct
                          ? "status-correct"
                          : "status-incorrect"
                      }`}
                    >
                      {item.is_correct
                        ? "✓ Correct"
                        : "✕ Incorrect"}
                    </span>
                  </div>

                  <h3>{item.question_text}</h3>

                  <div className="quiz-review-options">
                    {["A", "B", "C", "D"].map((option) => {
                      const isSelected =
                        item.selected_option === option;

                      const isCorrect =
                        item.correct_option === option;

                      let optionClass = "quiz-review-option";

                      if (isCorrect) {
                        optionClass += " correct-answer";
                      } else if (isSelected) {
                        optionClass += " wrong-answer";
                      }

                      return (
                        <div
                          className={optionClass}
                          key={option}
                        >
                          <span className="quiz-review-letter">
                            {option}
                          </span>

                          <span className="quiz-review-option-text">
                            {getOptionText(item, option)}
                          </span>

                          <span className="quiz-review-label">
                            {isCorrect
                              ? "Correct answer"
                              : isSelected
                                ? "Your answer"
                                : ""}
                          </span>
                        </div>
                      );
                    })}
                  </div>

                  <div className="quiz-review-explanation">
                    <strong>Explanation</strong>
                    <p>
                      {item.explanation ||
                        "No explanation is available for this question."}
                    </p>
                  </div>
                </article>
              ))}
            </div>
          ) : (
            <p className="quiz-review-empty">
              No answer review is available for this submission.
            </p>
          )}
        </section>
      </DashboardLayout>
    );
  }

  const currentQuestion = questions[currentIndex];

  if (!currentQuestion) {
    return (
      <DashboardLayout title="Quiz" subtitle="">
        <p>This quiz has no questions yet.</p>
      </DashboardLayout>
    );
  }

  const options = [
    ["A", currentQuestion.option_a],
    ["B", currentQuestion.option_b],
    ["C", currentQuestion.option_c],
    ["D", currentQuestion.option_d],
  ];

  return (
    <DashboardLayout
      title={quiz.title}
      subtitle={quiz.description || "Answer the questions below."}
    >
      <div className="quiz-attempt-card">
        <div className="quiz-question-header">
          <span>
            Question {currentIndex + 1} of {questions.length}
          </span>

          <span>
            {Object.keys(answers).length} answered
          </span>
        </div>

        <div className="quiz-question-progress">
          <div
            style={{
              width: `${((currentIndex + 1) / questions.length) * 100}%`,
            }}
          />
        </div>

        <h2>{currentQuestion.question_text}</h2>

        <div className="quiz-options">
          {options.map(([option, text]) => (
            <button
              key={option}
              className={
                answers[currentQuestion.id] === option
                  ? "quiz-option selected"
                  : "quiz-option"
              }
              onClick={() =>
                selectAnswer(currentQuestion.id, option)
              }
            >
              <span className="quiz-option-letter">
                {option}
              </span>
              <span>{text}</span>
            </button>
          ))}
        </div>

        {error && <p className="dashboard-error">{error}</p>}

        <div className="quiz-navigation">
          <button
            className="quiz-secondary-button"
            disabled={currentIndex === 0}
            onClick={() =>
              setCurrentIndex((previous) => previous - 1)
            }
          >
            Previous
          </button>

          {currentIndex < questions.length - 1 ? (
            <button
              className="quiz-start-button"
              onClick={() =>
                setCurrentIndex((previous) => previous + 1)
              }
            >
              Next
            </button>
          ) : (
            <button
              className="quiz-start-button"
              disabled={submitting}
              onClick={handleSubmit}
            >
              {submitting ? "Submitting..." : "Submit Quiz"}
            </button>
          )}
        </div>
      </div>
    </DashboardLayout>
  );
}

export default QuizAttempt;
