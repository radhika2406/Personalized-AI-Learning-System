import { useEffect, useState } from "react";
import api from "../services/api";
import "./QuizPerformanceChart.css";

const CHART_WIDTH = 760;
const CHART_HEIGHT = 280;

const PLOT = {
  left: 48,
  right: 735,
  top: 20,
  bottom: 210,
};

function getSmoothPath(points) {
  if (points.length < 2) return "";

  let path = `M ${points[0].x} ${points[0].y}`;

  for (let i = 0; i < points.length - 1; i++) {
    const current = points[i];
    const next = points[i + 1];
    const distance = next.x - current.x;

    path += ` C ${current.x + distance * 0.4} ${current.y},
      ${next.x - distance * 0.4} ${next.y},
      ${next.x} ${next.y}`;
  }

  return path;
}

function QuizPerformanceChart() {
  const [attempts, setAttempts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    let isMounted = true;

    const fetchAttempts = async () => {
      try {
        setLoading(true);
        setError("");

        const response = await api.get("/quiz-attempts/me");

        if (isMounted) {
          setAttempts(Array.isArray(response.data) ? response.data : []);
        }
      } catch (err) {
        if (isMounted) {
          setError(
            err.response?.data?.detail ||
              "Unable to load quiz performance."
          );
        }
      } finally {
        if (isMounted) {
          setLoading(false);
        }
      }
    };

    fetchAttempts();

    return () => {
      isMounted = false;
    };
  }, []);

  const chartData = attempts
    .filter(
      (attempt) =>
        attempt.submitted_at &&
        attempt.total_questions > 0 &&
        Number.isFinite(Number(attempt.score))
    )
    .sort(
      (a, b) =>
        new Date(a.submitted_at).getTime() -
        new Date(b.submitted_at).getTime()
    )
    .map((attempt, index) => ({
      id: attempt.id,
      quizId: attempt.quiz_id,
      date: new Date(attempt.submitted_at),
      percentage: Math.max(
        0,
        Math.min(
          100,
          (Number(attempt.score) / Number(attempt.total_questions)) * 100
        )
      ),
      score: attempt.score,
      totalQuestions: attempt.total_questions,
      attemptNumber: index + 1,
    }));

  const averageScore =
    chartData.length > 0
      ? chartData.reduce((sum, item) => sum + item.percentage, 0) /
        chartData.length
      : 0;

   const latestScore = chartData.length
   ? chartData[chartData.length - 1].percentage
   : 0;

  const bestScore = chartData.length
   ? Math.max(...chartData.map((item) => item.percentage))
   : 0;

  const previousScore =
   chartData.length > 1
    ? chartData[chartData.length - 2].percentage
    : null;

  const scoreChange =
   previousScore === null ? null : latestScore - previousScore;   

  const points = chartData.map((item, index) => {
    const x =
      chartData.length === 1
        ? (PLOT.left + PLOT.right) / 2
        : PLOT.left +
          (index / (chartData.length - 1)) *
            (PLOT.right - PLOT.left);

    const y =
      PLOT.bottom -
      (item.percentage / 100) * (PLOT.bottom - PLOT.top);

    return { ...item, x, y };
  });

  const linePath = getSmoothPath(points);
  const areaPath =
    points.length > 1
      ? `${linePath} L ${points[points.length - 1].x} ${PLOT.bottom} L ${points[0].x} ${PLOT.bottom} Z`
      : "";

  const labelIndexes =
    points.length <= 5
      ? points.map((_, index) => index)
      : [
          0,
          Math.round((points.length - 1) / 4),
          Math.round((points.length - 1) / 2),
          Math.round((3 * (points.length - 1)) / 4),
          points.length - 1,
        ];

  if (loading) {
    return (
      <section className="quiz-performance-card">
        <div className="quiz-chart-heading">
          <div>
            <h2>Quiz Performance</h2>
            <p>Your scores will appear here as you complete quizzes.</p>
          </div>
        </div>
        <div className="quiz-chart-loading">
          <span className="chart-loader" />
          Loading your performance...
        </div>
      </section>
    );
  }

  if (error) {
    return (
      <section className="quiz-performance-card">
        <div className="quiz-chart-heading">
          <div>
            <h2>Quiz Performance</h2>
            <p>Track how your scores change over time.</p>
          </div>
        </div>
        <p className="quiz-chart-message error">{error}</p>
      </section>
    );
  }

  return (
    <section className="quiz-performance-card">
      <div className="quiz-chart-heading">
        <div>
          <span className="quiz-chart-eyebrow">YOUR PROGRESS</span>
          <h2>Quiz Performance</h2>
          <p>See how your quiz scores improve over time.</p>
        </div>

        <div className="quiz-average">
          <span>Average score</span>
          <strong>{averageScore.toFixed(1)}%</strong>
        </div>
      </div>

      {chartData.length === 0 ? (
        <div className="quiz-chart-empty">
          <div className="quiz-empty-icon">✦</div>
          <h3>Your progress starts here</h3>
          <p>
            Complete your first quiz and your performance curve will appear
            here.
          </p>
        </div>
      ) : (
        <>
          <div className="quiz-chart-metrics">
                    <div className="quiz-metric">
                    <span className="metric-icon">✦</span>
                    <div>
                    <span>Latest score</span>
                    <strong>{latestScore.toFixed(1)}%</strong>
                    </div>
                    </div>

                    <div className="quiz-metric">
                    <span className="metric-icon">↗</span>
                    <div>
                    <span>Best score</span>
                    <strong>{bestScore.toFixed(1)}%</strong>
                    </div>
                    </div>

                    <div className="quiz-metric">
                    <span className="metric-icon">⌁</span>
                    <div>
                    <span>Change from previous</span>
                    <strong className={
                    scoreChange === null
                    ? ""
                    : scoreChange > 0
                    ? "metric-positive"
                    : scoreChange < 0
                    ? "metric-negative"
                    : ""
                    }>
                    {scoreChange === null
                    ? "—"
                    : `${scoreChange > 0 ? "+" : ""}${scoreChange.toFixed(1)} pts`}
                    </strong>
                    </div>
                    </div>
                    </div>

          <div className="quiz-chart-container">
            <svg
              className="quiz-performance-svg"
              viewBox={`0 0 ${CHART_WIDTH} ${CHART_HEIGHT}`}
              role="img"
              aria-label="Quiz scores over time"
            >
              <defs>
                <linearGradient
                  id="quizLineGradient"
                  x1="0"
                  y1="0"
                  x2="1"
                  y2="0"
                >
                  <stop offset="0%" stopColor="#7053D6" />
                  <stop offset="100%" stopColor="#B7A7F5" />
                </linearGradient>

                <linearGradient
                  id="quizAreaGradient"
                  x1="0"
                  y1="0"
                  x2="0"
                  y2="1"
                >
                  <stop
                    offset="0%"
                    stopColor="#9277E5"
                    stopOpacity="0.32"
                  />
                  <stop
                    offset="100%"
                    stopColor="#9277E5"
                    stopOpacity="0.015"
                  />
                </linearGradient>
              </defs>

              {[0, 25, 50, 75, 100].map((value) => {
                const y =
                  PLOT.bottom -
                  (value / 100) * (PLOT.bottom - PLOT.top);

                return (
                  <g key={value}>
                    <line
                      x1={PLOT.left}
                      y1={y}
                      x2={PLOT.right}
                      y2={y}
                      className="quiz-chart-gridline"
                    />
                    <text
                      x={PLOT.left - 12}
                      y={y + 4}
                      textAnchor="end"
                      className="quiz-chart-axis-label"
                    >
                      {value}%
                    </text>
                  </g>
                );
              })}

              {points.length > 1 && (
                <path
                  d={areaPath}
                  fill="url(#quizAreaGradient)"
                  className="quiz-chart-area"
                />
              )}

              {points.length > 1 && (
                <path
                  d={linePath}
                  fill="none"
                  stroke="url(#quizLineGradient)"
                  strokeWidth="2.5"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  pathLength="1"
                  className="quiz-chart-line"
                />
              )}
              {points.length > 0 && (
                    <g className="quiz-chart-latest">
                    <circle
                    cx={points[points.length - 1].x}
                    cy={points[points.length - 1].y}
                    r="11"
                    className="quiz-chart-pulse"
                    />
                    <circle
                    cx={points[points.length - 1].x}
                    cy={points[points.length - 1].y}
                    r="4"
                    className="quiz-chart-latest-dot"
                    />
                    </g>
                    )}

              {points.map((point, index) => (
                <g
                  key={point.id}
                  className="quiz-chart-point"
                  style={{ animationDelay: `${0.8 + index * 0.08}s` }}
                >
                  <circle
                    cx={point.x}
                    cy={point.y}
                    r="10"
                    className="quiz-chart-point-glow"
                  />
                  <circle
                    cx={point.x}
                    cy={point.y}
                    r="5"
                    className="quiz-chart-point-dot"
                  />
                  <title>
                    Quiz #{point.quizId} |{" "}
                    {point.date.toLocaleDateString()} |{" "}
                    {point.percentage.toFixed(1)}% |{" "}
                    {point.score}/{point.totalQuestions}
                  </title>
                </g>
              ))}

              {labelIndexes.map((index) => {
                const point = points[index];

                return (
                  <text
                    key={point.id}
                    x={point.x}
                    y="245"
                    textAnchor="middle"
                    className="quiz-chart-axis-label"
                  >
                    {point.date.toLocaleDateString(undefined, {
                    day: "numeric",
                    month: "short",
                    })}
                    {" "}
                    {point.date.toLocaleTimeString(undefined, {
                    hour: "2-digit",
                    minute: "2-digit",
                    })}
                  </text>
                );
              })}
            </svg>
          </div>

          <div className="quiz-chart-footer">
            <span>
              <span className="quiz-chart-legend-dot" />
              Performance per quiz attempt
            </span>
            <span>Latest: {points[points.length - 1].percentage.toFixed(1)}%</span>
          </div>
        </>
      )}
    </section>
  );
}

export default QuizPerformanceChart;
