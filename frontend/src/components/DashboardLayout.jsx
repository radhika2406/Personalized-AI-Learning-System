import { NavLink, useNavigate } from "react-router-dom";
import {
  LayoutDashboard,
  BookOpen,
  FileText,
  ClipboardList,
  Lightbulb,
  UserRound,
  LogOut,
} from "lucide-react";
import "./DashboardLayout.css";

function DashboardLayout({ title, subtitle, children }) {
  const navigate = useNavigate();

  const navigation = [
    { name: "Dashboard", path: "/dashboard", icon: LayoutDashboard },
    { name: "My Courses", path: "/courses", icon: BookOpen },
    { name: "Learning Materials", path: "/materials", icon: FileText },
    { name: "Quizzes", path: "/quizzes", icon: ClipboardList },
  {
      name: "Quiz History",
      path: "/quiz-history",
      icon: ClipboardList,
    },
    { name: "Recommendations", path: "/recommendations", icon: Lightbulb },
    { name: "My Profile", path: "/profile", icon: UserRound },
    
    {
      name: "Learning Path",
      path: "/learning-path",
      icon: BookOpen,
    },
  ];

  const handleLogout = () => {
    localStorage.removeItem("token");
    navigate("/login");
  };

  return (
    <div className="dashboard-layout">
      <aside className="dashboard-sidebar">
        <div className="sidebar-brand">
          <span className="brand-icon">L</span>
          <span>Learnova</span>
        </div>

        <p className="sidebar-label">MENU</p>

        <nav className="sidebar-navigation">
          {navigation.map((item) => {
            const Icon = item.icon;

            return (
              <NavLink
                key={item.name}
                to={item.path}
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

        <button className="logout-button" onClick={handleLogout}>
          <LogOut size={20} />
          <span>Logout</span>
        </button>
      </aside>

      <main className="dashboard-main">
        <header className="dashboard-header">
          <div>
            <h1>{title}</h1>
            <p>{subtitle}</p>
          </div>
        </header>

        {children}
      </main>
    </div>
  );
}

export default DashboardLayout;
