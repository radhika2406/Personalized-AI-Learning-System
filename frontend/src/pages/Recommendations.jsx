
import { useEffect, useState } from "react";
import DashboardLayout from "../components/DashboardLayout";
import api from "../services/api";
import "./Recommendations.css";

function Recommendations() {
  const [recommendations, setRecommendations] = useState([]);
  const [courses, setCourses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [generating, setGenerating] = useState(false);
  const [error, setError] = useState("");

  const fetchRecommendations = async () => {
    try {
      const [recommendationsResponse, coursesResponse] =
        await Promise.all([
          api.get("/recommendations/me"),
          api.get("/courses/"),
        ]);

      setRecommendations(recommendationsResponse.data);
      setCourses(coursesResponse.data);
      setError("");
    } catch (err) {
      setError(
        err.response?.data?.detail ||
          "Failed to load recommendations."
      );
    } finally {
      setLoading(false);
    }
  };

  const generateRecommendations = async () => {
    try {
      setGenerating(true);
      setError("");

      await api.post("/recommendations/generate");
      await fetchRecommendations();
    } catch (err) {
      setError(
        err.response?.data?.detail ||
          "Failed to generate recommendations."
      );
    } finally {
      setGenerating(false);
    }
  };

  const updateStatus = async (id, status) => {
    try {
      setError("");

      await api.patch(`/recommendations/${id}/status`, {
        status,
      });

      await fetchRecommendations();
    } catch (err) {
      setError(
        err.response?.data?.detail ||
          "Failed to update recommendation."
      );
    }
  };

  useEffect(() => {
    fetchRecommendations();
  }, []);

  return (
    <DashboardLayout
      title="Recommendations"
      subtitle="Personalized suggestions to improve your learning."
    >
      <div className="recommendations-page">

        {/* Generate recommendations */}
        <button
          className="recommendations-generate-button"
          onClick={generateRecommendations}
          disabled={generating}
        >
          <span>{generating ? "⏳" : "✦"}</span>
          {generating
            ? "Generating Recommendations..."
            : "Generate Recommendations"}
        </button>

        {/* Error */}
        {error && (
          <p className="recommendations-error" role="alert">
            {error}
          </p>
        )}

        {/* Loading */}
        {loading ? (
          <div className="recommendations-loading">
            Loading your recommendations...
          </div>
        ) : recommendations.length === 0 ? (

          /* Empty state */
          <div className="recommendations-empty">
            <h3>No Recommendations Yet</h3>
            <p>
              Your personalized learning suggestions will
              appear here. Click Generate Recommendations
              to get started.
            </p>
          </div>

        ) : (

          /* Recommendations list */
          <div className="recommendations-list">
            {recommendations.map((item) => {
              const course = courses.find(
                (course) => course.id === item.course_id
              );

              const status = String(
                item.status || "pending"
              ).toLowerCase();

              return (
                <article
                  key={item.id}
                  className="recommendation-card"
                >
                  <h3>{item.title}</h3>

                  <p>
                    <strong>Course:</strong>{" "}
                    {course?.title || "Course unavailable"}
                  </p>

                  <p className="recommendation-description">
                    {item.description}
                  </p>

                  {item.reason && (
                    <p>
                      <strong>Why this is recommended:</strong>{" "}
                      {item.reason}
                    </p>
                  )}

                  <div className="recommendation-meta">
                    <span className="recommendation-type">
                      {item.recommendation_type}
                    </span>

                    <span
                      className={`recommendation-status status-${status}`}
                    >
                      {item.status}
                    </span>
                  </div>

                  {/* Recommendation actions */}
                  {status === "pending" && (
                    <div className="recommendation-actions">
                      <button
                        className="recommendation-accept-button"
                        onClick={() =>
                          updateStatus(item.id, "accepted")
                        }
                      >
                        Accept
                      </button>

                      <button
                        className="recommendation-dismiss-button"
                        onClick={() =>
                          updateStatus(item.id, "dismissed")
                        }
                      >
                        Dismiss
                      </button>
                    </div>
                  )}

                  {status === "accepted" && (
                    <div className="recommendation-actions">
                      <button
                        className="recommendation-complete-button"
                        onClick={() =>
                          updateStatus(item.id, "completed")
                        }
                      >
                        Mark as Completed
                      </button>
                    </div>
                  )}
                </article>
              );
            })}
          </div>
        )}
      </div>
    </DashboardLayout>
  );
}

export default Recommendations;
