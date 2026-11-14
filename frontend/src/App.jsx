import React, { useState } from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";

import Login from "./pages/Login";
import Register from "./pages/Register";
import Home from "./pages/Home";
import { UserProvider } from "./UserContext";

import Dashboard from "./dashboard.jsx";
import Courses from "./pages/Courses";
import CourseDetails from "./pages/CourseDetails";
import LearningMaterials from "./pages/LearningMaterials";
import Quizzes from "./pages/Quizzes";
import QuizAttempt from "./pages/QuizAttempt";
import QuizHistory from "./pages/QuizHistory";
import Recommendations from "./pages/Recommendations";
import Profile from "./pages/Profile";
import LearningPath from "./pages/LearningPath";
import CategoryCourses from "./pages/CategoryCourses";

import { ThemeProvider } from "./ThemeContext";
import ProtectedRoute from "./components/ProtectedRoute";
import OnboardingWelcome from "./pages/OnboardingWelcome";
import OnboardingPreferences from "./pages/OnboardingPreferences";

import "./App.css";

function App() {
  const [showIntro, setShowIntro] = useState(true);

  const handleIntroComplete = () => {
    setShowIntro(false);
  };

  return (
    <ThemeProvider>
      <UserProvider>
      <BrowserRouter>
        <Routes>
          {/* Public routes */}
          <Route
            path="/"
            element={
              <Home
                showIntro={showIntro}
                onIntroComplete={handleIntroComplete}
              />
            }
          />

          <Route path="/register" element={<Register />} />
          <Route path="/login" element={<Login />} />
          <Route
            path="/categories/:categoryCode"
            element={<CategoryCourses />}
          />
          <Route path="/courses/:courseId" element={<CourseDetails />} />

          {/* Protected routes */}
          <Route element={<ProtectedRoute />}>
            <Route path="/onboarding" element={<OnboardingWelcome />} />

            <Route
              path="/onboarding/preferences"
              element={<OnboardingPreferences />}
            />

            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/courses" element={<Courses />} />
            <Route path="/materials" element={<LearningMaterials />} />

            <Route
              path="/topics/:topicId/materials"
              element={<LearningMaterials />}
            />

            <Route path="/quizzes" element={<Quizzes />} />

            <Route
              path="/quizzes/:quizId/attempt"
              element={<QuizAttempt />}
            />

            <Route path="/quiz-history" element={<QuizHistory />} />
            <Route path="/recommendations" element={<Recommendations />} />
            <Route path="/profile" element={<Profile />} />
            <Route path="/learning-path" element={<LearningPath />} />
          </Route>
        </Routes>
      </BrowserRouter>
      </UserProvider>
    </ThemeProvider>
  );
}

export default App;
