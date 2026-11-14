import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import {
  ArrowLeft,
  ArrowRight,
  Brain,
  BookOpen,
  Clock3,
  Target,
  Sparkles,
  Sun,
  Moon,
  GraduationCap,
  CheckCircle2,
} from "lucide-react";

import { useTheme } from "../ThemeContext";
import api from "../services/api";
import "./OnboardingPreferences.css";

const options = {
  learnerCategory: [
    "School Student",
    "College Student",
    "University Student",
    "Working Professional",
    "Self-Learner",
    "Other",
  ],

  educationLevel: [
    "School",
    "Diploma",
    "Undergraduate",
    "Postgraduate",
    "Graduate",
    "Doctoral / PhD",
    "Not Currently Studying",
    "Other",
  ],

  currentLevel: [
    "Complete Beginner",
    "Beginner",
    "Intermediate",
    "Advanced",
    "Expert",
    "Not Sure",
    "Other",
  ],

  dailyStudy: [
    { label: "15 minutes", value: 15 },
    { label: "30 minutes", value: 30 },
    { label: "45 minutes", value: 45 },
    { label: "1 hour", value: 60 },
    { label: "90 minutes", value: 90 },
    { label: "2 hours", value: 120 },
    { label: "3+ hours", value: 180 },
    { label: "Flexible / Varies", value: 60 },
    { label: "Other", value: "other" },
  ],

  learningGoals: [
    "Improve Academic Performance",
    "Prepare for Placements",
    "Prepare for Competitive Exams",
    "Learn Programming",
    "Develop Practical Skills",
    "Build Projects",
    "Career Advancement",
    "Explore New Subjects",
  ],

  interests: [
    "Artificial Intelligence",
    "Machine Learning",
    "Web Development",
    "Data Science",
    "Python",
    "Java",
    "Cybersecurity",
    "Cloud Computing",
    "App Development",
    "Data Structures & Algorithms",
  ],

  learningStyles: [
    "Video Lessons",
    "Reading Notes",
    "Step-by-Step Tutorials",
    "Coding Exercises",
    "Quizzes",
    "Hands-on Projects",
    "Interactive Activities",
    "Live Sessions",
  ],

  studyDays: [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
  ],

  learningTargets: [
    "Complete a Course",
    "Prepare for Exams",
    "Learn a Skill in 30 Days",
    "Build a Project",
    "Prepare for Interviews",
    "No Specific Deadline",
    "Other",
  ],
};

function CheckboxGroup({ title, items, selected, onChange }) {
  const toggleOption = (item) => {
    onChange(
      selected.includes(item)
        ? selected.filter((value) => value !== item)
        : [...selected, item]
    );
  };

  return (
    <div className="onboarding-checkbox-grid">
      {items.map((item) => (
        <label
          key={item}
          className={`onboarding-checkbox-option ${
            selected.includes(item) ? "selected" : ""
          }`}
        >
          <input
            type="checkbox"
            checked={selected.includes(item)}
            onChange={() => toggleOption(item)}
          />
          <span>{item}</span>
          {selected.includes(item) && (
            <CheckCircle2 size={17} />
          )}
        </label>
      ))}
    </div>
  );
}

function OnboardingPreferences() {
  const navigate = useNavigate();
  const { theme, toggleTheme } = useTheme();

  const [courses, setCourses] = useState([]);
  const [loadingCourses, setLoadingCourses] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");
  const [isEditing, setIsEditing] = useState(false);

  const [learnerCategory, setLearnerCategory] = useState("");
  const [learnerCategoryCustom, setLearnerCategoryCustom] = useState("");

  const [educationLevel, setEducationLevel] = useState("");
  const [educationCustom, setEducationCustom] = useState("");

  const [currentLevel, setCurrentLevel] = useState("");
  const [currentLevelCustom, setCurrentLevelCustom] = useState("");

  const [dailyStudy, setDailyStudy] = useState("60");
  const [dailyStudyCustom, setDailyStudyCustom] = useState("");

  const [learningGoals, setLearningGoals] = useState([]);
  const [learningGoalsCustom, setLearningGoalsCustom] = useState("");

  const [interests, setInterests] = useState([]);
  const [interestsCustom, setInterestsCustom] = useState("");

  const [learningStyles, setLearningStyles] = useState([]);
  const [learningStylesCustom, setLearningStylesCustom] = useState("");

  const [courseId, setCourseId] = useState("");
  const [courseCustom, setCourseCustom] = useState("");

  const [studyDays, setStudyDays] = useState([]);
  const [studyDaysCustom, setStudyDaysCustom] = useState("");
  const allStudyDaysSelected = options.studyDays.every((day) =>
    studyDays.includes(day)
  );

  const handleAllStudyDaysChange = (event) => {
    setStudyDays(
      event.target.checked ? [...options.studyDays] : []
    );
  };

  const [studySchedule, setStudySchedule] = useState("");

  const [learningTarget, setLearningTarget] = useState("");
  const [learningTargetCustom, setLearningTargetCustom] = useState("");

  useEffect(() => {
    const fetchCourses = async () => {
      try {
        const response = await api.get("/courses/");
        setCourses(response.data);
      } catch (err) {
        console.error("Unable to load courses:", err);
      } finally {
        setLoadingCourses(false);
      }
    };

    fetchCourses();
  }, []);

useEffect(() => {
  const fetchExistingProfile = async () => {
    try {
      const response = await api.get("/learner-profiles/me");
      const data = response.data;

      setIsEditing(true);

      const custom = data.custom_answers || {};

      setLearnerCategory(
        options.learnerCategory.includes(data.learner_category)
          ? data.learner_category
          : "Other"
      );
      setLearnerCategoryCustom(
        custom.learner_category ||
        (options.learnerCategory.includes(data.learner_category)
          ? ""
          : data.learner_category || "")
      );

      setEducationLevel(
        options.educationLevel.includes(data.education_level)
          ? data.education_level
          : data.education_level
            ? "Other"
            : ""
      );
      setEducationCustom(custom.education_level || "");

      setCurrentLevel(
        options.currentLevel.includes(data.current_level)
          ? data.current_level
          : "Other"
      );
      setCurrentLevelCustom(
        custom.current_level ||
        (options.currentLevel.includes(data.current_level)
          ? ""
          : data.current_level || "")
      );

      setDailyStudy(
        data.daily_study_custom
          ? "other"
          : String(data.daily_study_minutes || 60)
      );
      setDailyStudyCustom(data.daily_study_custom || "");

      setLearningGoals(data.learning_goals || []);
      setLearningGoalsCustom(custom.learning_goals || "");

      setInterests(data.interest_topics || []);
      setInterestsCustom(custom.interests || "");

      setLearningStyles(data.learning_styles || []);
      setLearningStylesCustom(custom.learning_styles || "");

      setCourseId(data.course_id ? String(data.course_id) : "");
      setCourseCustom(data.course_custom || "");

      setStudyDays(
        data.preferred_study_days || []
      );
      setStudyDaysCustom(custom.preferred_study_days || "");

      setStudySchedule(data.preferred_study_schedule || "");

      setLearningTarget(
        options.learningTargets.includes(data.learning_target)
          ? data.learning_target
          : data.learning_target
            ? "Other"
            : ""
      );
      setLearningTargetCustom(
        custom.learning_target ||
        (options.learningTargets.includes(data.learning_target)
          ? ""
          : data.learning_target || "")
      );
    } catch (err) {
      if (err.response?.status === 404) {
        setIsEditing(false);
      } else {
        console.error("Unable to load existing profile:", err);
        setError("Unable to load your saved learning preferences.");
      }
    }
  };

  fetchExistingProfile();
}, []);


  const customAnswers = {
    learner_category: learnerCategoryCustom.trim(),
    education_level: educationCustom.trim(),
    current_level: currentLevelCustom.trim(),
    learning_goals: learningGoalsCustom.trim(),
    interests: interestsCustom.trim(),
    learning_styles: learningStylesCustom.trim(),
    preferred_study_days: studyDaysCustom.trim(),
    learning_target: learningTargetCustom.trim(),
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError("");

    const finalCategory =
      learnerCategory === "Other"
        ? learnerCategoryCustom.trim()
        : learnerCategory;

    const finalLevel =
      currentLevel === "Other"
        ? currentLevelCustom.trim()
        : currentLevel;

    const finalGoals = [
      ...learningGoals,
      ...(learningGoalsCustom.trim()
        ? [learningGoalsCustom.trim()]
        : []),
    ];

    if (!finalCategory || !finalLevel) {
      setError("Please complete your learner category and current level.");
      return;
    }

    if (!finalGoals.length) {
      setError("Please select or enter at least one learning goal.");
      return;
    }

    if (educationLevel === "Other" && !educationCustom.trim()) {
      setError("Please specify your education level.");
      return;
    }

    if (dailyStudy === "other" && !dailyStudyCustom.trim()) {
      setError("Please specify your daily study time.");
      return;
    }

    if (learningTarget === "Other" && !learningTargetCustom.trim()) {
      setError("Please specify your learning target.");
      return;
    }

    if (learnerCategory === "Other" && !finalCategory) {
      setError("Please specify your learner category.");
      return;
    }

    if (currentLevel === "Other" && !finalLevel) {
      setError("Please specify your current level.");
      return;
    }

    const selectedDailyOption = options.dailyStudy.find(
      (item) => String(item.value) === dailyStudy
    );

    const dailyMinutes =
      selectedDailyOption?.value === "other"
        ? 60
        : Number(selectedDailyOption?.value || 60);

    const selectedCourse = courses.find(
      (course) => course.id === Number(courseId)
    );

    const finalInterests = [
      ...interests,
      ...(interestsCustom.trim()
        ? [interestsCustom.trim()]
        : []),
    ];

    try {
      setSaving(true);

      const payload = {
        learner_category: finalCategory,
        current_level: finalLevel,
        daily_study_minutes: dailyMinutes,
        daily_study_custom:
          dailyStudy === "other" ? dailyStudyCustom.trim() : null,

        learning_goal: finalGoals.join(", "),
        learning_goals: finalGoals,

        interests: finalInterests.join(", "),
        interest_topics: finalInterests,

        education_level:
          educationLevel === "Other"
            ? educationCustom.trim()
            : educationLevel || null,

        learning_styles: [
          ...learningStyles,
          ...(learningStylesCustom.trim()
            ? [learningStylesCustom.trim()]
            : []),
        ],

        course_id: courseId ? Number(courseId) : null,
        course_custom: courseCustom.trim() || null,

        preferred_study_days: [
          ...studyDays,
          ...(studyDaysCustom.trim()
            ? [studyDaysCustom.trim()]
            : []),
        ],

        preferred_study_schedule: studySchedule.trim() || null,

        learning_target:
          learningTarget === "Other"
            ? learningTargetCustom.trim()
            : learningTarget || null,

        custom_answers: customAnswers,
      };

      if (isEditing) {
                    await api.patch("/learner-profiles/me", payload);
                    } else {
                    await api.post("/learner-profiles/", payload);
                    }

      navigate("/dashboard", { replace: true });
    } catch (err) {
      setError(
        err.response?.data?.detail ||
          "Unable to save your learning preferences. Please try again."
      );
    } finally {
      setSaving(false);
    }
  };

  return (
    <div
      className="auth-modern onboarding-preferences"
      data-theme={theme}
    >
      <div className="auth-ambient auth-ambient-one" />
      <div className="auth-ambient auth-ambient-two" />

      <button
        className="auth-theme-toggle"
        onClick={toggleTheme}
        type="button"
        aria-label="Toggle theme"
      >
        {theme === "dark" ? <Sun size={20} /> : <Moon size={20} />}
      </button>

      <div className="auth-brand">
        <span className="auth-brand-icon">
          <Brain size={23} />
        </span>
        Learnova
      </div>

      <main className="onboarding-form-container">
        <button
          type="button"
          className="onboarding-back-button"
          onClick={() => navigate("/onboarding")}
        >
          <ArrowLeft size={17} />
          Back
        </button>

        <div className="onboarding-form-heading">
          <div className="onboarding-icon">
            <Sparkles size={28} />
          </div>

          <p className="onboarding-eyebrow">
            YOUR PERSONALIZED LEARNING JOURNEY
          </p>

          <h1>
                    {isEditing
                    ? "Update Your Learning Profile"
                    : "Tell Us About Yourself"}
          </h1>

          <p>
                    {isEditing
                    ? "Update your interests, goals, knowledge level, and study preferences."
                    : "Help us understand your learning needs so we can create a learning experience that works for you."}
                    </p>
        </div>

        <form
          className="onboarding-preferences-form"
          onSubmit={handleSubmit}
        >
          {error && (
            <div className="onboarding-form-error" role="alert">
              {error}
            </div>
          )}

          <section className="onboarding-section">
            <div className="onboarding-section-heading">
              <GraduationCap size={21} />
              <div>
                <h2>About You</h2>
                <p>Tell us about your educational background.</p>
              </div>
            </div>

            <div className="onboarding-field">
              <label>Which category describes you best?</label>
              <select
                value={learnerCategory}
                onChange={(e) => setLearnerCategory(e.target.value)}
                required
              >
                <option value="">Select your category</option>
                {options.learnerCategory.map((item) => (
                  <option key={item} value={item}>{item}</option>
                ))}
              </select>

              {learnerCategory === "Other" && (
                <input
                  value={learnerCategoryCustom}
                  onChange={(e) => setLearnerCategoryCustom(e.target.value)}
                  placeholder="Enter your learner category"
                  required
                />
              )}
            </div>

            <div className="onboarding-field">
              <label>What is your current education level?</label>
              <select
                value={educationLevel}
                onChange={(e) => setEducationLevel(e.target.value)}
              >
                <option value="">Select education level</option>
                {options.educationLevel.map((item) => (
                  <option key={item} value={item}>{item}</option>
                ))}
              </select>

              {educationLevel === "Other" && (
                <input
                  value={educationCustom}
                  onChange={(e) => setEducationCustom(e.target.value)}
                  placeholder="Enter your education level"
                />
              )}
            </div>

            <div className="onboarding-field">
              <label>How would you describe your current knowledge?</label>
              <select
                value={currentLevel}
                onChange={(e) => setCurrentLevel(e.target.value)}
                required
              >
                <option value="">Select your knowledge level</option>
                {options.currentLevel.map((item) => (
                  <option key={item} value={item}>{item}</option>
                ))}
              </select>

              {currentLevel === "Other" && (
                <input
                  value={currentLevelCustom}
                  onChange={(e) => setCurrentLevelCustom(e.target.value)}
                  placeholder="Describe your knowledge level"
                  required
                />
              )}
            </div>
          </section>

          <section className="onboarding-section">
            <div className="onboarding-section-heading">
              <Target size={21} />
              <div>
                <h2>Your Learning Goals</h2>
                <p>What would you like to achieve? Select all that apply.</p>
              </div>
            </div>

            <CheckboxGroup
              items={options.learningGoals}
              selected={learningGoals}
              onChange={setLearningGoals}
            />

            <div className="onboarding-field">
              <label>Have another learning goal?</label>
              <input
                value={learningGoalsCustom}
                onChange={(e) => setLearningGoalsCustom(e.target.value)}
                placeholder="Write your own learning goal..."
              />
            </div>
          </section>

          <section className="onboarding-section">
            <div className="onboarding-section-heading">
              <Brain size={21} />
              <div>
                <h2>Your Interests</h2>
                <p>Which subjects or technologies interest you?</p>
              </div>
            </div>

            <CheckboxGroup
              items={options.interests}
              selected={interests}
              onChange={setInterests}
            />

            <div className="onboarding-field">
              <label>Any other interests?</label>
              <input
                value={interestsCustom}
                onChange={(e) => setInterestsCustom(e.target.value)}
                placeholder="Add your own interests..."
              />
            </div>
          </section>

          <section className="onboarding-section">
            <div className="onboarding-section-heading">
              <BookOpen size={21} />
              <div>
                <h2>Learning Preferences</h2>
                <p>How do you prefer to learn?</p>
              </div>
            </div>

            <CheckboxGroup
              items={options.learningStyles}
              selected={learningStyles}
              onChange={setLearningStyles}
            />

            <div className="onboarding-field">
              <label>Other preferred learning methods?</label>
              <input
                value={learningStylesCustom}
                onChange={(e) => setLearningStylesCustom(e.target.value)}
                placeholder="Describe another learning method..."
              />
            </div>
          </section>

          <section className="onboarding-section">
            <div className="onboarding-section-heading">
              <Clock3 size={21} />
              <div>
                <h2>Your Study Routine</h2>
                <p>Tell us about your available study time.</p>
              </div>
            </div>

            <div className="onboarding-field">
              <label>How much time can you study daily?</label>
              <select
                value={dailyStudy}
                onChange={(e) => setDailyStudy(e.target.value)}
              >
                {options.dailyStudy.map((item) => (
                  <option key={item.label} value={item.value}>
                    {item.label}
                  </option>
                ))}
              </select>

              {dailyStudy === "other" && (
                <input
                  value={dailyStudyCustom}
                  onChange={(e) => setDailyStudyCustom(e.target.value)}
                  placeholder="Enter your available study time"
                />
              )}
            </div>
            <div className="onboarding-field">
              <label>Which days are you available to study?</label>

              <div className="onboarding-checkbox-grid">
                {options.studyDays.map((day) => (
                  <label
                    key={day}
                    className={`onboarding-checkbox-option ${
                      studyDays.includes(day) ? "selected" : ""
                    }`}
                  >
                    <input
                      type="checkbox"
                      checked={studyDays.includes(day)}
                      onChange={() =>
                        setStudyDays((previous) =>
                          previous.includes(day)
                            ? previous.filter((item) => item !== day)
                            : [...previous, day]
                        )
                      }
                    />
                    <span>{day}</span>
                    {studyDays.includes(day) && (
                      <CheckCircle2 size={17} />
                    )}
                  </label>
                ))}

                <label
                  className={`onboarding-checkbox-option ${
                    allStudyDaysSelected ? "selected" : ""
                  }`}
                >
                  <input
                    type="checkbox"
                    checked={allStudyDaysSelected}
                    onChange={handleAllStudyDaysChange}
                  />
                  <span>All Days</span>
                  {allStudyDaysSelected && (
                    <CheckCircle2 size={17} />
                  )}
                </label>
              </div>
            </div>
            <div className="onboarding-field">
              <label>Any specific study schedule? (Optional)</label>
              <textarea
                value={studySchedule}
                onChange={(e) => setStudySchedule(e.target.value)}
                placeholder="Example: Weekdays after 7 PM, weekends in the morning..."
                rows={3}
              />
            </div>

            <div className="onboarding-field">
              <label>Any other study-day preferences?</label>
              <input
                value={studyDaysCustom}
                onChange={(e) => setStudyDaysCustom(e.target.value)}
                placeholder="Enter any additional availability..."
              />
            </div>
          </section>

          <section className="onboarding-section">
            <div className="onboarding-section-heading">
              <BookOpen size={21} />
              <div>
                <h2>Course & Learning Target</h2>
                <p>Choose what you want to focus on.</p>
              </div>
            </div>

            <div className="onboarding-field">
              <label>Which course would you like to focus on?</label>

              <select
                value={courseId}
                onChange={(e) => setCourseId(e.target.value)}
              >
                <option value="">No course selected</option>
                {loadingCourses ? (
                  <option disabled>Loading courses...</option>
                ) : (
                  courses.map((course) => (
                    <option key={course.id} value={course.id}>
                      {course.title}
                    </option>
                  ))
                )}
              </select>

              <input
                value={courseCustom}
                onChange={(e) => setCourseCustom(e.target.value)}
                placeholder="Or enter another course..."
              />
            </div>

            <div className="onboarding-field">
              <label>What is your learning target?</label>
              <select
                value={learningTarget}
                onChange={(e) => setLearningTarget(e.target.value)}
              >
                <option value="">Select your target</option>
                {options.learningTargets.map((item) => (
                  <option key={item} value={item}>{item}</option>
                ))}
              </select>

              {learningTarget === "Other" && (
                <input
                  value={learningTargetCustom}
                  onChange={(e) => setLearningTargetCustom(e.target.value)}
                  placeholder="Describe your learning target..."
                />
              )}
            </div>
          </section>

          <div className="onboarding-submit-area">
            <p>
              Your preferences can be updated anytime from My Profile.
            </p>

            <button
              type="submit"
              className="onboarding-primary-button"
              disabled={saving}
            >
             {saving
                    ? "Saving Your Preferences..."
                    : isEditing
                    ? "Update My Learning Profile"
                    : "Save My Learning Profile"}
              {!saving && <ArrowRight size={19} />}
            </button>

            <button
              type="button"
              className="onboarding-skip-button"
              onClick={() => navigate("/", { replace: true })}
              disabled={saving}
            >
              I'll Complete This Later
            </button>
          </div>
        </form>
      </main>
    </div>
  );
}

export default OnboardingPreferences;
