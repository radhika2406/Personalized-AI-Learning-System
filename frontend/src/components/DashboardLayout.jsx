import { useEffect, useRef, useState } from "react";
import { NavLink, useNavigate, Link } from "react-router-dom";
import {
  LayoutDashboard,
  BookOpen,
  FileText,
  ClipboardList,
  Lightbulb,
  UserRound,
  LogOut,
  Sun,
  Moon,
  Menu,
  X,
  ChevronDown,
} from "lucide-react";

import "./DashboardLayout.css";
import { useTheme } from "../ThemeContext";
import api from "../services/api";
import GlobalSearch from "./GlobalSearch";
import Logo from "./Logo";

function DashboardLayout({ title, subtitle, children }) {
  const navigate = useNavigate();
  const { theme, toggleTheme } = useTheme();

  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [profileOpen, setProfileOpen] = useState(false);
  const [account, setAccount] = useState(null);

  const profileRef = useRef(null);

  const navigation = [
    { name: "Dashboard", path: "/dashboard", icon: LayoutDashboard },
    { name: "My Courses", path: "/courses", icon: BookOpen },
    { name: "Learning Materials", path: "/materials", icon: FileText },
    { name: "Quizzes", path: "/quizzes", icon: ClipboardList },
    { name: "Quiz History", path: "/quiz-history", icon: ClipboardList },
    { name: "Recommendations", path: "/recommendations", icon: Lightbulb },
    { name: "My Profile", path: "/profile", icon: UserRound },
    { name: "Learning Path", path: "/learning-path", icon: BookOpen },
  ];

  useEffect(() => {
    let active = true;

    const fetchAccount = async () => {
      try {
        const response = await api.get("/users/me");

        if (active) {
          setAccount(response.data);
        }
      } catch (error) {
        console.error("Unable to load student account:", error);
      }
    };

    if (localStorage.getItem("token")) {
      fetchAccount();
    }

    return () => {
      active = false;
    };
  }, []);

  useEffect(() => {
    const handleKeyDown = (event) => {
      if (event.key === "Escape") {
        setSidebarOpen(false);
        setProfileOpen(false);
      }
    };

    window.addEventListener("keydown", handleKeyDown);

    return () => {
      window.removeEventListener("keydown", handleKeyDown);
    };
  }, []);

  useEffect(() => {
    if (sidebarOpen) {
      document.body.classList.add("sidebar-menu-open");
    } else {
      document.body.classList.remove("sidebar-menu-open");
    }

    return () => {
      document.body.classList.remove("sidebar-menu-open");
    };
  }, [sidebarOpen]);

  useEffect(() => {
    const handleOutsideClick = (event) => {
      if (
        profileRef.current &&
        !profileRef.current.contains(event.target)
      ) {
        setProfileOpen(false);
      }
    };

    document.addEventListener("mousedown", handleOutsideClick);

    return () => {
      document.removeEventListener("mousedown", handleOutsideClick);
    };
  }, []);

  const closeSidebar = () => {
    setSidebarOpen(false);
  };

  const handleLogout = () => {
    localStorage.removeItem("token");
    setProfileOpen(false);
    closeSidebar();
    navigate("/login");
  };

  const fullName = account?.full_name || "Learner";
  const email = account?.email || "";

  const initials = fullName
    .trim()
    .split(/\s+/)
    .slice(0, 2)
    .map((part) => part[0])
    .join("")
    .toUpperCase();

  const ProfileControl = () => (
    <div className="student-profile-wrapper" ref={profileRef}>
      <button
        type="button"
        className="student-profile-trigger"
        onClick={() => setProfileOpen((previous) => !previous)}
        aria-expanded={profileOpen}
        aria-label="Open student profile menu"
      >
        <span className="student-avatar">
          {initials || "L"}
        </span>

        <span className="student-greeting">
          <strong>Hi, {fullName.split(" ")[0]}!</strong>
          <small>Welcome back</small>
        </span>

        <ChevronDown
          size={16}
          className={`profile-chevron ${profileOpen ? "profile-chevron-open" : ""}`}
        />
      </button>

      {profileOpen && (
        <div className="student-profile-dropdown">
          <div className="profile-dropdown-heading">
            <span className="student-avatar dropdown-avatar">
              {initials || "L"}
            </span>
            <span>
              <strong>{fullName}</strong>
              <small>{email}</small>
            </span>
          </div>

          <div className="profile-dropdown-divider" />

          <Link
            to="/profile"
            className="profile-dropdown-item"
            onClick={() => setProfileOpen(false)}
          >
            <UserRound size={17} />
            My Profile
          </Link>

          <button
            type="button"
            className="profile-dropdown-item profile-dropdown-logout"
            onClick={handleLogout}
          >
            <LogOut size={17} />
            Logout
          </button>
        </div>
      )}
    </div>
  );

  return (
    <div
      className="dashboard-layout"
      data-theme={theme}
    >

      {sidebarOpen && (
        <button
          type="button"
          className="sidebar-backdrop"
          onClick={closeSidebar}
          aria-label="Close navigation menu"
        />
      )}


      <aside
        id="dashboard-sidebar"
        className={`dashboard-sidebar ${
          sidebarOpen ? "sidebar-open" : ""
        }`}
      >
        <div className="sidebar-top">
          <Logo />
        </div>

        <button
          type="button"
          className="sidebar-close-button"
          onClick={closeSidebar}
          aria-label="Close navigation menu"
        >
          <X size={22} />
        </button>

        <p className="sidebar-label">MENU</p>

        <nav className="sidebar-navigation" aria-label="Main navigation">
          {navigation.map((item) => {
            const Icon = item.icon;

            return (
              <NavLink
                key={item.name}
                to={item.path}
                onClick={closeSidebar}
                className={({ isActive }) =>
                  isActive ? "nav-item active" : "nav-item"
                }
              >
                <Icon size={20} />
                <span>{item.name}</span>
              </NavLink>
            );
          })}
        </nav>

        <button
          type="button"
          className="logout-button"
          onClick={handleLogout}
        >
          <LogOut size={20} />
          <span>Logout</span>
        </button>
      </aside>

      <main className="dashboard-main">

        <div className="mobile-topbar">
          <button
            type="button"
            className="mobile-menu-button"
            onClick={() => setSidebarOpen(true)}
            aria-label="Open navigation menu"
            aria-expanded={sidebarOpen}
            aria-controls="dashboard-sidebar"
          >
            <Menu size={23} />
          </button>

         <div className="mobile-brand">
            <Logo />
          </div>

          <div className="mobile-profile-area">
            <ProfileControl />

            <button
              type="button"
              className="theme-toggle mobile-theme-toggle"
              onClick={toggleTheme}
              aria-label="Toggle theme"
            >
              {theme === "dark" ? (
                <Sun size={19} />
              ) : (
                <Moon size={19} />
              )}
            </button>
          </div>
        </div>

        <header className="dashboard-header">
      <div className="dashboard-heading">
        <h1>{title}</h1>
        <p>{subtitle}</p>
      </div>

      <GlobalSearch />

          <div className="desktop-header-actions">
            <ProfileControl />

            <button
              type="button"
              className="theme-toggle desktop-theme-toggle"
              onClick={toggleTheme}
              aria-label="Toggle theme"
              title="Toggle dark/light mode"
            >
              {theme === "dark" ? (
                <Sun size={20} />
              ) : (
                <Moon size={20} />
              )}
            </button>
          </div>
        </header>

        {children}
      </main>
    </div>
  );
}

export default DashboardLayout;
