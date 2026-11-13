import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { GoogleLogin } from "@react-oauth/google";
import { Brain, ArrowRight, Sun, Moon } from "lucide-react";
import api from "../services/api";

function Register() {
  const navigate = useNavigate();

  const [theme, setTheme] = useState(
    localStorage.getItem("learnova-theme") || "dark"
  );

  const toggleTheme = () => {
    const nextTheme = theme === "dark" ? "light" : "dark";
    setTheme(nextTheme);
    localStorage.setItem("learnova-theme", nextTheme);
  };

  const [formData, setFormData] = useState({
    full_name: "",
    email: "",
    password: "",
  });

  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [googleLoading, setGoogleLoading] = useState(false);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  // Normal email and password registration

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      const response = await api.post("/users/register", formData);

      localStorage.setItem("token", response.data.access_token);

      navigate("/onboarding");
    } catch (err) {
      console.error("Registration error:", err.response?.data || err.message);

      const message = err.response?.data?.detail;

      setError(
        typeof message === "string"
          ? message
          : JSON.stringify(err.response?.data || err.message)
      );
    } finally {
      setLoading(false);
    }
  };


  // Google registration
  const handleGoogleSuccess = async (credentialResponse) => {
    setError("");
    setGoogleLoading(true);

    try {
      const response = await api.post("/auth/google", {
        credential: credentialResponse.credential,
      });

      localStorage.setItem("token", response.data.access_token);
      navigate(
        response.data.is_new_user ? "/onboarding" : "/",
        { replace: true }
      );
    } catch (err) {
      console.error(
        "Google registration error:",
        err.response?.data || err.message
      );

      const message = err.response?.data?.detail;

      setError(
        typeof message === "string"
          ? message
          : "Google registration failed. Please try again."
      );
    } finally {
      setGoogleLoading(false);
    }
  };

  return (
    <div className="auth-container auth-modern" data-theme={theme}>
      <div className="auth-ambient auth-ambient-one" />
      <div className="auth-ambient auth-ambient-two" />

      <button className="auth-theme-toggle" onClick={toggleTheme}>
        {theme === "dark" ? <Sun size={19} /> : <Moon size={19} />}
      </button>

      <Link to="/" className="auth-brand">
        <span className="auth-brand-icon">
          <Brain size={23} />
        </span>
        Learnova
      </Link>

      <div className="auth-card auth-card-modern">
        <div className="auth-heading-icon">
          <Brain size={25} />
        </div>

        <p className="auth-eyebrow">YOUR LEARNING JOURNEY STARTS HERE</p>
        <h1 className="auth-heading">Create Account</h1>
        <p className="auth-description">
          Create your account and discover learning built around you.
        </p>

        {error && <div className="auth-error">{error}</div>}

        {/* Google Registration */}
        <div className="google-login-section">
          {googleLoading ? (
            <p>Creating your account...</p>
          ) : (

          <GoogleLogin
            onSuccess={handleGoogleSuccess}
            onError={() =>
              setError("Google registration was unsuccessful. Please try again.")
            }
            theme={theme === "dark" ? "filled_blue" : "outline"}
            text="signup_with"
            shape="pill"
            size="large"
            width="350"
          />

          )}
        </div>

        <div className="auth-divider">
          <span>OR REGISTER WITH EMAIL</span>
        </div>

        {/* Normal Registration Form */}
        <form onSubmit={handleSubmit} className="auth-form-modern">
          <label htmlFor="full_name">Full Name</label>
          <input
            id="full_name"
            name="full_name"
            type="text"
            placeholder="Enter your full name"
            value={formData.full_name}
            onChange={handleChange}
            required
          />

          <label htmlFor="email">Email Address</label>
          <input
            id="email"
            name="email"
            type="email"
            placeholder="Enter your email"
            value={formData.email}
            onChange={handleChange}
            required
          />

          <label htmlFor="password">Password</label>
          <input
            id="password"
            name="password"
            type="password"
            placeholder="Create a password (min. 8 characters)"
            value={formData.password}
            onChange={handleChange}
            minLength={8}
            required
          />

          <button
            type="submit"
            className="auth-submit-modern"
            disabled={loading}
          >
            {loading ? (
              "Creating Account..."
            ) : (
              <>
                Create Account <ArrowRight size={17} />
              </>
            )}
          </button>
        </form>

        <p className="auth-footer-modern">
          Already have an account? <Link to="/login">Login</Link>
        </p>

        <Link to="/" className="auth-back-home">
          ← Back to Home
        </Link>
      </div>
    </div>
  );
}

export default Register;
