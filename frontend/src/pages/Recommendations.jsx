import { useEffect, useState } from "react";
import DashboardLayout from "../components/DashboardLayout";
import api from "../services/api";

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
      setError("Failed to load recommendations.");
    } finally {
        setLoading(false);
    }
  };

  const generateRecommendations = async () => {
    try {
      setGenerating(true);
      await api.post("/recommendations/generate");
      await fetchRecommendations();
    } catch (err) {
      setError("Failed to generate recommendations.");
    } finally {
      setGenerating(false);
    }
  };

  const updateStatus = async (id, status) => {
    try {
      await api.patch(`/recommendations/${id}/status`, {
        status,
      });
      await fetchRecommendations();
    } catch (err) {
      setError("Failed to update recommendation.");
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
        <button
          onClick={generateRecommendations}
          disabled={generating}
        >
          {generating
            ? "Generating..."
            : "Generate Recommendations"}
        </button>

        {error && <p>{error}</p>}

        {loading ? (
          <p>Loading recommendations...</p>
        ) : recommendations.length === 0 ? (
          <p>No recommendations yet. Click Generate Recommendations.</p>
        ) : (
          recommendations.map((item) => (
            <div key={item.id} className="recommendation-card">
              <h3>{item.title}</h3>
              <p>
                <strong>Course:</strong>{" "}
                {courses.find((course) => course.id === item.course_id)?.title
                  || "Course unavailable"}
              </p>
              <p>{item.description}</p>

              {item.reason && <p><strong>Reason:</strong> {item.reason}</p>}

              <p><strong>Type:</strong> {item.recommendation_type}</p>
              <p><strong>Status:</strong> {item.status}</p>

              {item.status === "pending" && (
                <>
                  <button onClick={() => updateStatus(item.id, "accepted")}>
                    Accept
                  </button>

                  <button onClick={() => updateStatus(item.id, "dismissed")}>
                    Dismiss
                  </button>
                </>
              )}

              {item.status === "accepted" && (
                <button onClick={() => updateStatus(item.id, "completed")}>
                  Mark Completed
                </button>
              )}
            </div>
          ))
        )}
      </div>
    </DashboardLayout>
  );
}

export default Recommendations;
