import { Brain } from "lucide-react";
import "./Logo.css";

function Logo() {
  return (
    <div className="learnova-logo">
      <div className="learnova-logo-icon">
        <Brain size={26} />
      </div>
      <span className="learnova-logo-text">Learnova</span>
    </div>
  );
}

export default Logo;
