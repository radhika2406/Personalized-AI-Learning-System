import sys
from pathlib import Path

# Add the project root to Python's module search path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import json
from pathlib import Path
from collections import defaultdict
from ai_engine.recommendation.study_planner import build_plan
from ai_engine.learner_analysis.analysis_pipeline import analyze_learner
from ai_engine.recommendation.topic_recommender import recommend_topics

# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent

LEARNERS_FILE = BASE_DIR / "data" / "learners.json"
ATTEMPTS_FILE = BASE_DIR / "data" / "quiz_attempts.json"
OUTPUT_FILE = BASE_DIR / "data" / "personalization_reports.json"

from ai_engine.learner_analysis.progress_tracking import (
    build_progress_report,
)

def load_json(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def main():
    learners = load_json(LEARNERS_FILE)
    quiz_attempts = load_json(ATTEMPTS_FILE)

    # Group quiz attempts by learner
    attempts_by_learner = defaultdict(list)

    for attempt in quiz_attempts:
        attempts_by_learner[attempt["learner_id"]].append(attempt)

    reports = []

    for profile in learners:
        learner_id = profile["learner_id"]
        course_id = profile["course"]

        learner_attempts = attempts_by_learner.get(learner_id, [])

        # Analyze this learner's performance and mastery
        analysis = analyze_learner(
            quiz_results=learner_attempts,
            course_id=course_id,
            learner_id=learner_id,
        )

        # Combine learner preferences with analysis results
        recommendation_input = {
            **profile,
            **analysis,
        }

        # Generate personalized topic recommendations
        recommendations = recommend_topics(recommendation_input)

        # Generate a daily study plan
        study_plan = build_plan(recommendation_input)

        # Generate overall learner progress
        progress_report = build_progress_report(
            quiz_results=learner_attempts,
            course_id=course_id,
            learner_id=learner_id,
        )

        report = {
            "learner_id": learner_id,
            "course": course_id,
            "profile": profile,
            "assessment_count": len(learner_attempts),
            "analysis": analysis,
            "recommendations": recommendations,
            "study_plan": study_plan,
            "progress_report": progress_report,
        }

        reports.append(report)

        print(f"Processed: {learner_id}")
        print(f"  Course: {course_id}")
        print(f"  Assessments: {len(learner_attempts)}")
        print(f"  Recommendations: {len(recommendations)}")

    # Save all learner reports
    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        json.dump(reports, file, indent=2, ensure_ascii=False)

    print("\nPersonalization pipeline completed!")
    print(f"Total learners processed: {len(reports)}")
    print(f"Reports saved to: {OUTPUT_FILE}")
    print(f"Daily budget: {study_plan['daily_minutes']} minutes")
    print(f"Planned time: {study_plan['total_minutes']} minutes")
    print(f"Topics scheduled: {len(study_plan['recommended_topics'])}")


if __name__ == "__main__":
    main()
