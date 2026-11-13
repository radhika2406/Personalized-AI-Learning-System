
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { Sparkles } from "lucide-react";
import DashboardLayout from "../components/DashboardLayout";
import api from "../services/api";
import "./Profile.css";

function Profile() {
  const navigate = useNavigate();
  const [profile, setProfile] = useState(null);
  const [savedProfile, setSavedProfile] = useState(null);
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

      const [coursesResponse, accountResponse] =
        await Promise.all([
          api.get("/courses/"),
          api.get("/users/me"),
        ]);

      setCourses(coursesResponse.data);
      setAccount(accountResponse.data);

      let profileData;

      try {
        const profileResponse = await api.get(
          "/learner-profiles/me"
        );

        profileData = profileResponse.data;
      } catch (err) {
        if (err.response?.status === 404) {
          profileData = null;
        } else {
          throw err;
        }
      }

      setProfile(profileData);
      setSavedProfile(profileData);
    } catch (err) {
      setError(
        err.response?.data?.detail ||
          "Failed to load profile."
      );
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (event) => {
    const { name, value } = event.target;

    setProfile((previous) => ({
      ...previous,
      [name]:
        name === "daily_study_minutes" ||
        name === "course_id"
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
      setSavedProfile(response.data);

      setMessage(
        profile.id
          ? "Profile updated successfully."
          : "Profile created successfully."
      );

      setIsEditing(false);
    } catch (err) {
      setError(
        err.response?.data?.detail ||
          "Failed to save profile."
      );
    } finally {
      setSaving(false);
    }
  };

  const handleCancel = () => {
    setProfile(savedProfile);
    setIsEditing(false);
    setError("");
    setMessage("");
  };

  useEffect(() => {
    fetchProfile();
  }, []);

  const initials = account?.full_name
    ? account.full_name
        .trim()
        .split(/\s+/)
        .slice(0, 2)
        .map((part) => part[0])
        .join("")
        .toUpperCase()
    : "L";

  const selectedCourse = courses.find(
    (course) => course.id === profile?.course_id
  );

  return (
    <DashboardLayout
      title="My Profile"
      subtitle="Manage your learning preferences and goals."
    >
      <div className="profile-page">
        {loading ? (
          <div className="profile-loading">
            <p>Loading your profile...</p>
          </div>
        ) : error && !profile ? (
          <div className="profile-unavailable">
            <p>{error}</p>
          </div>
        ) : (
          <>
            {/* Profile header */}
            <section className="profile-hero">
              <div className="profile-avatar">
                {initials}
              </div>

              <div className="profile-hero-info">
                <h2>
                  {account?.full_name || "Learner"}
                </h2>

                <p>
                  {account?.email || "Email not available"}
                </p>

                <span className="profile-hero-tag">
                  {profile?.learner_category?.replaceAll(
                    "_",
                    " "
                  ) || "Learner"}
                </span>
              </div>
            </section>

            {message && (
              <p className="profile-message" role="status">
                {message}
              </p>
            )}

            {error && (
              <p className="profile-error" role="alert">
                {error}
              </p>
            )}

            {!profile ? (
                <section className="profile-panel profile-incomplete">
                  <div className="profile-panel-header">
                    <div className="profile-panel-icon">
                      <Sparkles size={22} />
                    </div>

                    <div>
                      <h3>Complete Your Learning Profile</h3>
                      <p>Your personalized learning journey starts here.</p>
                    </div>
                  </div>

                  <div className="profile-incomplete-content">
                    <p>
                      You haven't set up your learning preferences yet.
                      Tell Learnova about your interests, goals, current
                      knowledge, and study routine so we can create a
                      learning experience tailored to your needs.
                    </p>

                    <button
                      type="button"
                      className="profile-edit-button"
                      onClick={() => navigate("/onboarding/preferences")}
                    >
                      Complete My Learning Profile
                    </button>
                  </div>
                </section>
              ) : !isEditing ? (
              /* Profile view */
              <div className="profile-content-grid">

                {/* Account information */}
                <section className="profile-panel">
                  <div className="profile-panel-header">
                    <div className="profile-panel-icon">
                      <span>👤</span>
                    </div>

                    <div>
                      <h3>Account Information</h3>
                      <p>Your registered account details</p>
                    </div>
                  </div>

                  <div className="profile-info-list">
                    <div className="profile-info-item">
                      <span className="profile-info-label">
                        Full Name
                      </span>
                      <span className="profile-info-value">
                        {account?.full_name || "Not available"}
                      </span>
                    </div>

                    <div className="profile-info-item">
                      <span className="profile-info-label">
                        Email Address
                      </span>
                      <span className="profile-info-value">
                        {account?.email || "Not available"}
                      </span>
                    </div>
                  </div>
                </section>

                {/* Learning profile */}
                <section className="profile-panel">
                  <div className="profile-panel-header">
                    <div className="profile-panel-icon">
                      <span>🎓</span>
                    </div>

                    <div>
                      <h3>Learning Preferences</h3>
                      <p>Your personalized learning details</p>
                    </div>
                  </div>


                  <div className="profile-info-list">

                    {/* 01 - About You */}
                    <div className="profile-preference-group">
                      <h4 className="profile-preference-group-title">
                        01. ABOUT YOU
                      </h4>

                      <div className="profile-info-list">
                        <div className="profile-info-item">
                          <span className="profile-info-label">Learner Category</span>
                          <span className="profile-info-value">
                            {profile.learner_category || "Not specified"}
                          </span>
                        </div>

                        <div className="profile-info-item">
                          <span className="profile-info-label">Education Level</span>
                          <span className="profile-info-value">
                            {profile.education_level || "Not specified"}
                          </span>
                        </div>

                        <div className="profile-info-item">
                          <span className="profile-info-label">Current Knowledge</span>
                          <span className="profile-info-value">
                            {profile.current_level || "Not specified"}
                          </span>
                        </div>

                        <div className="profile-info-item">
                          <span className="profile-info-label">Daily Study Time</span>
                          <span className="profile-info-value">
                            {profile.daily_study_custom ||
                              `${profile.daily_study_minutes} minutes`}
                          </span>
                        </div>
                      </div>
                    </div>

                    {/* 02 - Goals and Interests */}
                    <div className="profile-preference-group">
                      <h4 className="profile-preference-group-title">
                        02. GOALS & INTERESTS
                      </h4>

                      <div className="profile-info-list">
                        <div className="profile-info-item">
                          <span className="profile-info-label">Learning Goals</span>
                          <span className="profile-info-value">
                            {profile.learning_goals?.join(", ") ||
                              profile.learning_goal ||
                              "Not specified"}
                          </span>
                        </div>

                        <div className="profile-info-item">
                          <span className="profile-info-label">Interests</span>
                          <span className="profile-info-value">
                            {profile.interest_topics?.join(", ") ||
                              profile.interests ||
                              "Not specified"}
                          </span>
                        </div>
                      </div>
                    </div>

                    {/* 03 - Study Preferences */}
                    <div className="profile-preference-group">
                      <h4 className="profile-preference-group-title">
                        03. STUDY PREFERENCES
                      </h4>

                      <div className="profile-info-list">
                        <div className="profile-info-item">
                          <span className="profile-info-label">Learning Methods</span>
                          <span className="profile-info-value">
                            {profile.learning_styles?.join(", ") || "Not specified"}
                          </span>
                        </div>

                        <div className="profile-info-item">
                          <span className="profile-info-label">Preferred Study Days</span>
                          <span className="profile-info-value">
                            {profile.preferred_study_days?.join(", ") || "Not specified"}
                          </span>
                        </div>

                        <div className="profile-info-item">
                          <span className="profile-info-label">Study Schedule</span>
                          <span className="profile-info-value">
                            {profile.preferred_study_schedule || "Not specified"}
                          </span>
                        </div>

                        <div className="profile-info-item">
                          <span className="profile-info-label">Selected Course</span>
                          <span className="profile-info-value">
                            {selectedCourse?.title || "Not selected"}
                          </span>
                        </div>

                        {profile.course_custom && (
                          <div className="profile-info-item">
                            <span className="profile-info-label">Additional Course</span>
                            <span className="profile-info-value">
                              {profile.course_custom}
                            </span>
                          </div>
                        )}

                        <div className="profile-info-item">
                          <span className="profile-info-label">Learning Target</span>
                          <span className="profile-info-value">
                            {profile.learning_target || "Not specified"}
                          </span>
                        </div>
                      </div>
                    </div>

                  </div>


                  <button
                    type="button"
                    className="profile-edit-button"
                    onClick={() => navigate("/onboarding/preferences")}
                  >
                    Edit Learning Profile
                  </button>
                </section>
              </div>
            ) : (
              /* Edit profile form */
              <section className="profile-panel">
                <div className="profile-panel-header">
                  <div className="profile-panel-icon">
                    <span>✎</span>
                  </div>

                  <div>
                    <h3>Edit Learning Profile</h3>
                    <p>Update your learning preferences and goals</p>
                  </div>
                </div>

                <form
                  className="profile-form"
                  onSubmit={handleSave}
                >
                  <div className="profile-form-group">
                    <label htmlFor="learner_category">
                      Learner Category
                    </label>

                    <select
                      id="learner_category"
                      name="learner_category"
                      value={profile.learner_category}
                      onChange={handleChange}
                    >
                      <option value="college_student">
                        College Student
                      </option>
                      <option value="self_learner">
                        Self Learner
                      </option>
                      <option value="placement_learner">
                        Placement Learner
                      </option>
                    </select>
                  </div>

                  <div className="profile-form-group">
                    <label htmlFor="current_level">
                      Current Level
                    </label>

                    <select
                      id="current_level"
                      name="current_level"
                      value={profile.current_level}
                      onChange={handleChange}
                    >
                      <option value="beginner">Beginner</option>
                      <option value="intermediate">
                        Intermediate
                      </option>
                      <option value="advanced">Advanced</option>
                    </select>
                  </div>

                  <div className="profile-form-group">
                    <label htmlFor="daily_study_minutes">
                      Daily Study Minutes
                    </label>

                    <input
                      id="daily_study_minutes"
                      type="number"
                      name="daily_study_minutes"
                      min="1"
                      max="1440"
                      value={profile.daily_study_minutes}
                      onChange={handleChange}
                      required
                    />
                  </div>

                  <div className="profile-form-group">
                    <label htmlFor="course_id">
                      Preferred Course
                    </label>

                    <select
                      id="course_id"
                      name="course_id"
                      value={profile.course_id}
                      onChange={handleChange}
                      required
                    >
                      {courses.map((course) => (
                        <option
                          key={course.id}
                          value={course.id}
                        >
                          {course.title}
                        </option>
                      ))}
                    </select>
                  </div>

                  <div className="profile-form-group full-width">
                    <label htmlFor="learning_goal">
                      Learning Goal
                    </label>

                    <textarea
                      id="learning_goal"
                      name="learning_goal"
                      value={profile.learning_goal || ""}
                      onChange={handleChange}
                      placeholder="Describe your learning goal..."
                      required
                    />
                  </div>

                  <div className="profile-form-group full-width">
                    <label htmlFor="interests">
                      Interests
                    </label>

                    <textarea
                      id="interests"
                      name="interests"
                      value={profile.interests || ""}
                      onChange={handleChange}
                      placeholder="Enter your learning interests..."
                    />
                  </div>

                  <div className="profile-form-actions">
                    <button
                      type="submit"
                      className="profile-save-button"
                      disabled={saving}
                    >
                      {saving ? "Saving..." : "Save Profile"}
                    </button>

                    <button
                      type="button"
                      className="profile-cancel-button"
                      onClick={handleCancel}
                      disabled={saving}
                    >
                      Cancel
                    </button>
                  </div>
                </form>
              </section>
            )}
          </>
        )}
      </div>
    </DashboardLayout>
  );
}

export default Profile;
