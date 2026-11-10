import { useEffect, useState } from "react";
import DashboardLayout from "../components/DashboardLayout";
import api from "../services/api";

function Profile() {
  const [profile, setProfile] = useState(null);
  const [account, setAccount] = useState(null);
  const [isEditing, setIsEditing] = useState(false);
  const [courses, setCourses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  
  const fetchProfile = async () => {
    try {
      setLoading(true);
      setError("");

      const coursesResponse = await api.get("/courses/");
      setCourses(coursesResponse.data);
      const accountResponse = await api.get("/users/me");
      setAccount(accountResponse.data);

      try {
        const profileResponse = await api.get("/learner-profiles/me");
        setProfile(profileResponse.data);
      } catch (err) {
        if (err.response?.status === 404) {
          setProfile({
            learner_category: "college_student",
            current_level: "beginner",
            daily_study_minutes: 60,
            learning_goal: "",
            interests: "",
            course_id: coursesResponse.data[0]?.id || "",
          });
        } else {
          throw err;
        }
      }
    } catch (err) {
      setError(err.response?.data?.detail || "Failed to load profile.");
    } finally {
      setLoading(false);
    }
  };


  const handleChange = (event) => {
    const { name, value } = event.target;

    setProfile((previous) => ({
      ...previous,
      [name]:
        name === "daily_study_minutes" || name === "course_id"
          ? Number(value)
          : value,
    }));
  };

  
  const handleSave = async (event) => {
    event.preventDefault();

    try {
      setSaving(true);
      setMessage("");
      setError("");

      const payload = {
        learner_category: profile.learner_category,
        current_level: profile.current_level,
        daily_study_minutes: profile.daily_study_minutes,
        learning_goal: profile.learning_goal,
        interests: profile.interests,
        course_id: profile.course_id,
      };

      const response = profile.id
        ? await api.patch("/learner-profiles/me", payload)
        : await api.post("/learner-profiles/", payload);

      setProfile(response.data);
      setMessage(
        profile.id
          ? "Profile updated successfully."
          : "Profile created successfully."
      );
      setIsEditing(false);
    } catch (err) {
      setError(
        err.response?.data?.detail || "Failed to save profile."
      );
    } finally {
      setSaving(false);
    }
  };


  useEffect(() => {
    fetchProfile();
  }, []);

  return (
    <DashboardLayout
      title="My Profile"
      subtitle="Manage your learning preferences and goals."
    >
      <div className="profile-page">
        {loading ? (
          <p>Loading profile...</p>
        
          
          ) : !isEditing ? (
            
          <div className="profile-view">
              <h3>Account Information</h3>

              <p><strong>Full Name:</strong> {account?.full_name || "Not available"}</p>
              <p><strong>Email:</strong> {account?.email || "Not available"}</p>

              <hr />

              <h3>My Learning Profile</h3>


              <p><strong>Learner Category:</strong> {profile.learner_category}</p>
              <p><strong>Current Level:</strong> {profile.current_level}</p>
              <p><strong>Daily Study Minutes:</strong> {profile.daily_study_minutes}</p>
              <p><strong>Learning Goal:</strong> {profile.learning_goal}</p>
              <p><strong>Interests:</strong> {profile.interests || "Not specified"}</p>
              <p>
                <strong>Course:</strong>{" "}
                {courses.find((course) => course.id === profile.course_id)?.title || "Not selected"}
              </p>

              <button type="button" onClick={() => setIsEditing(true)}>
                Edit Profile
              </button>
            </div>
          ) : (
  

          <form onSubmit={handleSave}>
            <label>Learner Category</label>
            <select
              name="learner_category"
              value={profile.learner_category}
              onChange={handleChange}
            >
              <option value="college_student">College Student</option>
              <option value="self_learner">Self Learner</option>
              <option value="placement_learner">Placement Learner</option>
            </select>

            <label>Current Level</label>
            <select
              name="current_level"
              value={profile.current_level}
              onChange={handleChange}
            >
              <option value="beginner">Beginner</option>
              <option value="intermediate">Intermediate</option>
              <option value="advanced">Advanced</option>
            </select>

            <label>Daily Study Minutes</label>
            <input
              type="number"
              name="daily_study_minutes"
              min="1"
              max="1440"
              value={profile.daily_study_minutes}
              onChange={handleChange}
              required
            />

            <label>Learning Goal</label>
            <textarea
              name="learning_goal"
              value={profile.learning_goal}
              onChange={handleChange}
              required
            />

            <label>Interests</label>
            <textarea
              name="interests"
              value={profile.interests || ""}
              onChange={handleChange}
            />

            <label>Course</label>
            <select
              name="course_id"
              value={profile.course_id}
              onChange={handleChange}
              required
            >
              {courses.map((course) => (
                <option key={course.id} value={course.id}>
                  {course.title}
                </option>
              ))}
            </select>

            <button type="submit" disabled={saving}>
              {saving ? "Saving..." : "Save Profile"}
            </button>

            {message && <p>{message}</p>}
            {error && <p>{error}</p>}
          </form>
        )}
      </div>
    </DashboardLayout>
  );
}

export default Profile;
