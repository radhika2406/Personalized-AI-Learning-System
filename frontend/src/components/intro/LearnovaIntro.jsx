
import { useEffect, useRef, useState } from "react";
import {
  Brain,
  Atom,
  Code2,
  BookOpen,
  Sigma,
  Sparkles,
  ArrowRight,
  Orbit,
} from "lucide-react";
import { useTheme } from "../../ThemeContext";
import "./LearnovaIntro.css";

const floatingIcons = [
  { Icon: Brain, className: "intro-symbol symbol-one" },
  { Icon: Atom, className: "intro-symbol symbol-two" },
  { Icon: Code2, className: "intro-symbol symbol-three" },
  { Icon: BookOpen, className: "intro-symbol symbol-four" },
  { Icon: Sigma, className: "intro-symbol symbol-five" },
  { Icon: Sparkles, className: "intro-symbol symbol-six" },
];

function GalaxyCanvas() {
  const canvasRef = useRef(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    const reducedMotion = window.matchMedia(
      "(prefers-reduced-motion: reduce)"
    ).matches;

    let animationFrame;
    let width = 0;
    let height = 0;
    let stars = [];

    const resize = () => {
      const dpr = Math.min(window.devicePixelRatio || 1, 2);

      width = window.innerWidth;
      height = window.innerHeight;

      canvas.width = width * dpr;
      canvas.height = height * dpr;
      canvas.style.width = `${width}px`;
      canvas.style.height = `${height}px`;

      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);

      const count = width < 600 ? 100 : 220;

      stars = Array.from({ length: count }, () => ({
        x: Math.random() * width,
        y: Math.random() * height,
        radius: Math.random() * 1.5 + 0.3,
        opacity: Math.random() * 0.65 + 0.2,
        speed: Math.random() * 0.25 + 0.04,
        phase: Math.random() * Math.PI * 2,
      }));
    };

    const draw = (time = 0) => {
      ctx.clearRect(0, 0, width, height);

      stars.forEach((star) => {
        const twinkle = reducedMotion
          ? 1
          : 0.65 + Math.sin(time * 0.0015 + star.phase) * 0.35;

        ctx.beginPath();
        ctx.arc(star.x, star.y, star.radius, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(220, 220, 255, ${star.opacity * twinkle})`;
        ctx.fill();

        if (!reducedMotion) {
          star.y -= star.speed;

          if (star.y < -3) {
            star.y = height + 3;
            star.x = Math.random() * width;
          }
        }
      });

      if (!reducedMotion) {
        animationFrame = requestAnimationFrame(draw);
      }
    };

    resize();
    draw();

    window.addEventListener("resize", resize);

    return () => {
      cancelAnimationFrame(animationFrame);
      window.removeEventListener("resize", resize);
    };
  }, []);

  return <canvas ref={canvasRef} className="learnova-galaxy-canvas" />;
}

export default function LearnovaIntro({ onComplete }) {
  const { theme } = useTheme();
  const [exiting, setExiting] = useState(false);
  const [copyIndex, setCopyIndex] = useState(0);

  const messages = [
    "NOT EVERY MIND LEARNS THE SAME WAY.",
    "SO WHY SHOULD EVERYONE FOLLOW THE SAME PATH?",
    "YOUR INTELLIGENCE. YOUR PACE. YOUR UNIVERSE.",
  ];

  useEffect(() => {
    const reducedMotion = window.matchMedia(
      "(prefers-reduced-motion: reduce)"
    ).matches;

    if (reducedMotion) {
      setCopyIndex(2);
      return;
    }

    const first = window.setTimeout(() => setCopyIndex(1), 2800);
    const second = window.setTimeout(() => setCopyIndex(2), 5600);

    return () => {
      window.clearTimeout(first);
      window.clearTimeout(second);
    };
  }, []);

  const enterUniverse = () => {
    if (exiting) return;

    setExiting(true);

    const reducedMotion = window.matchMedia(
      "(prefers-reduced-motion: reduce)"
    ).matches;

    window.setTimeout(onComplete, reducedMotion ? 0 : 1150);
  };

  return (
    <section
      className={`learnova-intro ${theme === "light" ? "intro-light" : "intro-dark"} ${exiting ? "intro-exiting" : ""}`}
      aria-label="Welcome to Learnova"
    >
      <GalaxyCanvas />

      <div className="intro-nebula intro-nebula-one" />
      <div className="intro-nebula intro-nebula-two" />

      <button
        className="intro-skip-button"
        type="button"
        onClick={onComplete}
      >
        Skip Intro <ArrowRight size={15} />
      </button>

      <div className="intro-content">
        <div className="intro-orbit-scene">
          <div className="intro-orbit orbit-a" />
          <div className="intro-orbit orbit-b" />
          <div className="intro-orbit orbit-c" />

          <div className="intro-portal">
            <div className="portal-core">
              <div className="portal-core-inner">
                <Orbit size={54} strokeWidth={1.2} />
              </div>
            </div>
          </div>

          {floatingIcons.map(({ Icon, className }) => (
            <div className={className} key={className}>
              <Icon size={25} strokeWidth={1.5} />
            </div>
          ))}
        </div>

        <div className="intro-brand">
          <div className="intro-brand-mark">
            <Brain size={25} />
          </div>
          <h1>LEARNOVA</h1>
        </div>

        <div className="intro-tagline" aria-live="polite">
          <p key={copyIndex}>{messages[copyIndex]}</p>
        </div>

        <p className="intro-subtitle">
          A universe of learning, designed around you.
        </p>

        <button
          className="intro-enter-button"
          type="button"
          onClick={enterUniverse}
          disabled={exiting}
        >
          <span>ENTER YOUR UNIVERSE</span>
          <ArrowRight size={19} />
        </button>

        <div className="intro-bottom-note">
          <span className="intro-live-dot" />
          YOUR JOURNEY. YOUR DISCOVERY.
        </div>
      </div>
    </section>
  );
}
