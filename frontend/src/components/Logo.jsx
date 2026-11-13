
import { Brain } from "lucide-react";
import { Link } from "react-router-dom";
import "./Logo.css";

function Logo() {
  return (
    <Link
      to="/"
      className="learnova-logo"
      aria-label="Go to Learnova home page"
    >
      <div className="learnova-logo-icon">
        <Brain size={26} />
      </div>

      <span className="learnova-logo-text">
        Learnova
      </span>
    </Link>
  );
}

export default Logo;
