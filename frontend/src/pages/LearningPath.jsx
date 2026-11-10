
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import DashboardLayout from "../components/DashboardLayout";
import api from "../services/api";
import "./LearningPath.css";

function LearningPath() {
  const [courses, setCourses] = useState([]);
  const [selectedCourse, setSelectedCourse] = useState("");
  const [path, setPath] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const navigate = useNavigate();

  const totalMaterials = path.reduce(
    (sum, topic) => sum + topic.total_materials,
    0
  );

  const completedMaterials = path.reduce(
    (sum, topic) => sum + topic.completed_materials,
    0
  );

  const courseProgress =
    totalMaterials > 0
      ? Math.round((completedMaterials / totalMaterials) * 100)
      : 0;

  // Mark a material as completed
  const markMaterialCompleted = async (materialId) => {
    try {
      await api.put(`/learning-progress/material/${materialId}`, {
        status: "completed",
      });

      const response = await api.get(
        `/learning-path/course/${selectedCourse}`
      );

      setPath(response.data.learning_path);
    } catch (error) {
      console.error("Failed to complete material:", error);
      alert("Failed to update material progress.");
    }
  };

  // Fetch enrolled courses
  useEffect(() => {
    const fetchCourses = async () => {
      try {
        const response = await api.get("/enrollments/me");
        const enrolledCourses = response.data;

        setCourses(enrolledCourses);

        if (enrolledCourses.length > 0) {
          setSelectedCourse(String(enrolledCourses[0].course_id));
        }
      } catch (err) {
        setError("Failed to load enrolled courses.");
      }
    };

    fetchCourses();
  }, []);

  // Fetch learning path
  useEffect(() => {
    if (!selectedCourse) return;

    const fetchPath = async () => {
      try {
        setLoading(true);
        setError("");

        const response = await api.get(
          `/learning-path/course/${selectedCourse}`
        );

        setPath(response.data.learning_path);
      } catch (err) {
        setPath([]);
        setError(
          err.response?.data?.detail ||
            "Failed to load learning path."
        );
      } finally {
        setLoading(false);
      }
    };

    fetchPath();
  }, [selectedCourse]);

  return (
    <DashboardLayout
      title="Personalized Learning Path"
      subtitle="Follow your learning journey topic by topic."
    >
      <div className="learning-path-page">
        <label>Select Course</label>

        <select
          value={selectedCourse}
          onChange={(e) => setSelectedCourse(e.target.value)}
        >
          {courses.map((course) => (
            <option
              key={course.course_id}
              value={course.course_id}
            >
              {course.course_title ||
                course.title ||
                `Course ${course.course_id}`}
            </option>
          ))}
        </select>

        {loading && <p>Loading learning path...</p>}
        {error && <p>{error}</p>}

        {!loading && path.length > 0 && (
          <div className="course-progress">
            <h3>Overall Course Progress</h3>

            <p>
              {completedMaterials} / {totalMaterials} materials completed
            </p>

            <div className="progress-bar">
              <div
                className="progress-fill"
                style={{ width: `${courseProgress}%` }}
              />
            </div>

            <p>{courseProgress}% Completed</p>
          </div>
        )}

        {!loading &&
          path.map((topic) => (
            <div
              className="learning-path-topic"
              key={topic.topic_id}
            >
              <div className={`topic-heading ${topic.status}`}>
                <span className="topic-status-icon">
                  {topic.status === "completed"
                    ? "✓"
                    : topic.status === "current"
                    ? "●"
                    : "○"}
                </span>

                <h3>
                  {topic.sequence_number}. {topic.topic_title}
                </h3>

                <span className="topic-status-label">
                  {topic.status === "completed"
                    ? "Completed"
                    : topic.status === "current"
                    ? "Current Topic"
                    : "Upcoming"}
                </span>
              </div>

              <p>Status: {topic.status}</p>

              <p>
                Progress: {topic.completed_materials}/
                {topic.total_materials} materials completed (
                {topic.completion_percentage}%)
              </p>

              {topic.materials.map((material) => (
                <div key={material.material_id}>
                  <span>
                    {material.title} — {material.status}
                  </span>

                  <button
                    type="button"
                    onClick={() =>
                      navigate(
                        `/topics/${topic.topic_id}/materials`
                      )
                    }
                  >
                    Open Materials
                  </button>

                  {material.status !== "completed" && (
                    <button
                      type="button"
                      onClick={() =>
                        markMaterialCompleted(material.material_id)
                      }
                    >
                      Mark Completed
                    </button>
                  )}

                  {material.status === "completed" && (
                    <span> ✓ Completed</span>
                  )}
                </div>
              ))}
            </div>
          ))}
      </div>
    </DashboardLayout>
  );
}

export default LearningPath;
