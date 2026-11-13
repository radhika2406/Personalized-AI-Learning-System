
import {
  Brain,
  ArrowRight,
  Sun,
  Moon,
  Clock3,
  Target,
  BookOpen,
  Sparkles,
} from "lucide-react";

import { useNavigate } from "react-router-dom";
import { useTheme } from "../ThemeContext";
import "./OnboardingWelcome.css";

function OnboardingWelcome() {
  const navigate = useNavigate();
  const { theme, toggleTheme } = useTheme();

  const handleContinue = () => {
    navigate("/onboarding/preferences");
  };

  const handleSkip = () => {
    navigate("/dashboard");
  };

  return (
    <div className="auth-modern onboarding-welcome" data-theme={theme}>
      <div className="auth-ambient auth-ambient-one"></div>
      <div className="auth-ambient auth-ambient-two"></div>

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

      <main className="onboarding-welcome-card">
        <div className="onboarding-icon">
          <Sparkles size={30} />
        </div>

        <p className="onboarding-eyebrow">
          YOUR JOURNEY, YOUR WAY
        </p>

        <h1>Let's Personalize Your Learning!</h1>

        <p className="onboarding-description">
          Your learning journey starts with you. Tell us about your
          interests, goals, current knowledge, and study preferences.
          These details will help Learnova understand your learning
          needs and recommend a more relevant, focused, and effective
          learning experience.
        </p>

        <p className="onboarding-description">
          The more we know about your preferences, the better we can
          tailor your learning journey.
        </p>

        <div className="onboarding-benefits">
          <div className="onboarding-benefit">
            <Target size={21} />
            <span>Learning goals</span>
          </div>

          <div className="onboarding-benefit">
            <BookOpen size={21} />
            <span>Interests and subjects</span>
          </div>

          <div className="onboarding-benefit">
            <Brain size={21} />
            <span>Learning preferences</span>
          </div>
        </div>

        <div className="onboarding-time">
          <Clock3 size={17} />
          <span>Takes approximately 3–5 minutes</span>
        </div>

        <button
          className="onboarding-primary-button"
          onClick={handleContinue}
        >
          Let's Set Up My Learning Profile
          <ArrowRight size={19} />
        </button>

        <button
          className="onboarding-skip-button"
          onClick={handleSkip}
        >
          I'll Do This Later
        </button>

        <p className="onboarding-footer">
          You can complete or update your learning preferences
          anytime from My Profile.
        </p>
      </main>
    </div>
  );
}

export default OnboardingWelcome;
