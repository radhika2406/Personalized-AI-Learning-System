import { useState } from "react";
import { Link, useNavigate, useLocation } from "react-router-dom";
import { Brain, ArrowRight, Sun, Moon } from "lucide-react";
import { GoogleLogin } from "@react-oauth/google";
import api from "../services/api";

function Login() {
  const navigate = useNavigate();
  const location = useLocation();

  const enrollmentRedirect =
  location.state?.enrollmentIntent &&
  location.state?.from?.pathname
    ? location.state.from.pathname
    : "/";

  const [theme, setTheme] = useState(
    () => localStorage.getItem("learnova-theme") || "dark"
  );

  const [formData, setFormData] = useState({
    email: "",
    password: "",
  });

  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [googleLoading, setGoogleLoading] = useState(false);

  const toggleTheme = () => {
    const newTheme = theme === "dark" ? "light" : "dark";
    setTheme(newTheme);
    localStorage.setItem("learnova-theme", newTheme);
  };

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      const response = await api.post("/auth/login", formData);

      localStorage.setItem("token", response.data.access_token);

      navigate(enrollmentRedirect, { replace: true });
    } catch (err) {
      const message = err.response?.data?.detail;

      setError(
        typeof message === "string"
          ? message
          : "Login failed. Please check your credentials."
      );
    } finally {
      setLoading(false);
    }
  };

  const handleGoogleSuccess = async (credentialResponse) => {
    setError("");
    setGoogleLoading(true);

    try {
      const response = await api.post("/auth/google", {
        credential: credentialResponse.credential,
      });

      localStorage.setItem("token", response.data.access_token);
     navigate(
        response.data.is_new_user
          ? "/onboarding"
          : enrollmentRedirect,
        { replace: true }
      );
    } catch (err) {
      const message = err.response?.data?.detail;

      setError(
        typeof message === "string"
          ? message
          : "Google login failed. Please try again."
      );
    } finally {
      setGoogleLoading(false);
    }
  };

  return (
    <div className="auth-container auth-modern" data-theme={theme}>
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

      <Link to="/" className="auth-brand">
        <span className="auth-brand-icon">
          <Brain size={23} />
        </span>
        <span>Learnova</span>
      </Link>

      <div className="auth-card auth-card-modern">

        <h1 className="auth-heading">Welcome Back</h1>

        <p className="auth-description">
          Continue your personalized learning journey.
        </p>

        {error && <div className="auth-error">{error}</div>}


        <div className="google-login-section">
          {googleLoading ? (
            <p className="auth-description">Signing in with Google...</p>
          ) : (
            <GoogleLogin
              onSuccess={handleGoogleSuccess}
              onError={() => {
                setError("Google sign-in was unsuccessful. Please try again.");
              }}
              text="continue_with"
              shape="pill"
              theme={theme === "dark" ? "filled_blue" : "outline"}
              size="large"
              width="350"
            />
          )}
        </div>


        <div className="auth-divider">
          <span>OR CONTINUE WITH EMAIL</span>
        </div>

        <form onSubmit={handleSubmit} className="auth-form-modern">
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
            placeholder="Enter your password"
            value={formData.password}
            onChange={handleChange}
            required
          />

          <button
            type="submit"
            className="auth-submit-modern"
            disabled={loading || googleLoading}
          >
            {loading ? "Logging in..." : "Login"}
            {!loading && <ArrowRight size={18} />}
          </button>
        </form>

        <p className="auth-footer-modern">
          Don't have an account? <Link to="/register">Create Account</Link>
        </p>

        <p className="auth-footer-modern">
          <Link to="/">← Back to Home</Link>
        </p>
      </div>
    </div>
  );
}

export default Login;
