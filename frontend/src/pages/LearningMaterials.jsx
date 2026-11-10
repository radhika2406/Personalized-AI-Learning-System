import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import DashboardLayout from "../components/DashboardLayout";
import "./LearningMaterials.css";
import api from "../services/api";

function LearningMaterials() {
  const { topicId } = useParams();

  const [groups, setGroups] = useState([]);
  const [progress, setProgress] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [updatingId, setUpdatingId] = useState(null);

  useEffect(() => {
    const fetchMaterials = async () => {
      setLoading(true);
      setError("");

      try {
        let materialGroups = [];

        // Mode 1: Materials of one selected topic
        if (topicId) {
          const response = await api.get(
            `/learning-materials/topic/${topicId}`
          );

          materialGroups = [
            {
              courseTitle: "Learning Materials",
              topicTitle: "Selected Topic",
              materials: response.data,
            },
          ];
        } else {
          // Mode 2: Materials across enrolled courses
          const [enrollmentResponse, coursesResponse] =
            await Promise.all([
              api.get("/enrollments/me"),
              api.get("/courses/"),
            ]);

          const enrolledCourseIds =
            enrollmentResponse.data.map(
              (enrollment) => enrollment.course_id
            );

          const enrolledCourses =
            coursesResponse.data.filter((course) =>
              enrolledCourseIds.includes(course.id)
            );

          materialGroups = await Promise.all(
            enrolledCourses.map(async (course) => {
              const topicsResponse = await api.get(
                `/dashboard/course/${course.id}/topics`
              );

              const topics = topicsResponse.data;

              const topicGroups = await Promise.all(
                topics.map(async (topic) => {
                  const materialsResponse = await api.get(
                    `/learning-materials/topic/${topic.topic_id}`
                  );

                  return {
                    courseTitle: course.title,
                    topicTitle: topic.topic_title,
                    materials: materialsResponse.data,
                  };
                })
              );

              return topicGroups;
            })
          );

          materialGroups = materialGroups.flat();
        }

        setGroups(materialGroups);

        const allMaterials = materialGroups.flatMap(
          (group) => group.materials
        );

        const progressResults = await Promise.all(
          allMaterials.map(async (material) => {
            try {
              const result = await api.get(
                `/learning-progress/material/${material.id}`
              );

              return [material.id, result.data.status];
            } catch (err) {
              if (err.response?.status === 404) {
                return [material.id, "not_started"];
              }
              throw err;
            }
          })
        );

        setProgress(Object.fromEntries(progressResults));
      } catch (err) {
        setError(
          err.response?.data?.detail ||
            "Unable to load learning materials"
        );
      } finally {
        setLoading(false);
      }
    };

    fetchMaterials();
  }, [topicId]);

  const handleComplete = async (materialId) => {
    setUpdatingId(materialId);
    setError("");

    try {
      const response = await api.put(
        `/learning-progress/material/${materialId}`,
        { status: "completed" }
      );

      setProgress((previous) => ({
        ...previous,
        [materialId]: response.data.status,
      }));
    } catch (err) {
      setError(
        err.response?.data?.detail ||
          "Unable to update learning progress"
      );
    } finally {
      setUpdatingId(null);
    }
  };

  if (loading) {
    return <p>Loading learning materials...</p>;
  }

  
return (
  <DashboardLayout
    title="Learning Materials"
    subtitle="Explore your course materials and track your learning progress."
  >
    {error && <p>{error}</p>}

    {groups.length === 0 ? (
      <p>No learning materials available.</p>
    ) : (
      groups.map((group, index) => (
        <section
          key={`${group.courseTitle}-${group.topicTitle}-${index}`}
          className="materials-topic-section"
        >
          <h2>{group.courseTitle}</h2>
          <h3>{group.topicTitle}</h3>

          <div className="materials-grid">
            {group.materials.map((material) => {
              const isCompleted =
                progress[material.id] === "completed";

              return (
                <article
                  key={material.id}
                  className="material-card"
                >
                  <h4>{material.title}</h4>

                  <span className="material-type">
                    {material.material_type}
                  </span>

                  <p>{material.content}</p>

                  <button
                    className={
                      isCompleted
                        ? "material-completed-button"
                        : "material-complete-button"
                    }
                    disabled={
                      isCompleted ||
                      updatingId === material.id
                    }
                    onClick={() => handleComplete(material.id)}
                  >
                    {isCompleted
                      ? "✓ Completed"
                      : updatingId === material.id
                      ? "Saving..."
                      : "Mark as Completed"}
                  </button>
                </article>
              );
            })}
          </div>
        </section>
      ))
    )}
  </DashboardLayout>
);

}

export default LearningMaterials;
