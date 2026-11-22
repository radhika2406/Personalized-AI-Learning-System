
"""
targeted_revision.py

Generates personalized revision quizzes using learner mastery scores.
Reuses the existing course question bank.
"""

from typing import Any

from ai_engine.common.course_config import get_course
from assessment.question_management.loader import (
    load_course_topics,
    get_questions_by_topic,
)


def _validate_question_count(count: int) -> None:
    if isinstance(count, bool) or not isinstance(count, int) or count < 1:
        raise ValueError("questions_per_topic must be a positive integer")


def _get_revision_difficulty(score: float) -> str:
    """Choose a suitable revision difficulty based on mastery."""
    if score < 40:
        return "easy"
    if score < 60:
        return "medium"
    return "hard"


def _get_difficulty_fallbacks(difficulty: str) -> list[str]:
    """Provide alternative difficulties when the preferred level is unavailable."""
    fallbacks = {
        "easy": ["medium", "hard"],
        "medium": ["easy", "hard"],
        "hard": ["medium", "easy"],
    }
    return [difficulty] + fallbacks[difficulty]


def _select_questions(
    course_id: str,
    topic_id: str,
    difficulty: str,
    questions_per_topic: int,
) -> list[dict[str, Any]]:
    """Select questions at the preferred difficulty, with fallbacks."""

    selected = []
    used_question_ids = set()

    for level in _get_difficulty_fallbacks(difficulty):
        available = get_questions_by_topic(
            course_id,
            topic_id,
            difficulty=level,
        )

        for question in available:
            question_id = question.get("question_id")

            if question_id in used_question_ids:
                continue

            selected.append(question)
            used_question_ids.add(question_id)

            if len(selected) >= questions_per_topic:
                return selected

    return selected


def generate_targeted_revision(
    analysis: dict[str, Any],
    questions_per_topic: int = 3,
) -> dict[str, Any]:
    """
    Generate a revision quiz for topics where learner mastery is below 60%.

    Expected analysis fields:
        {
            "learner_id": "learner_01",
            "course": "python",
            "mastery": {
                "variables": 85,
                "conditions": 35,
                "loops": 50,
                "functions": None
            }
        }
    """

    if not isinstance(analysis, dict):
        raise ValueError("analysis must be a dictionary")

    _validate_question_count(questions_per_topic)

    course_id = analysis.get("course") or analysis.get("course_id")

    if not course_id or not get_course(course_id):
        raise ValueError("A valid course ID is required")

    mastery = analysis.get("mastery")

    if not isinstance(mastery, dict):
        raise ValueError("analysis must contain a mastery dictionary")

    valid_topics = {
        topic.get("id") or topic.get("topic_id")
        for topic in load_course_topics(course_id)
    }

    revision_topics = []

    for topic_id, raw_score in mastery.items():
        if topic_id not in valid_topics or raw_score is None:
            continue

        if isinstance(raw_score, bool) or not isinstance(raw_score, (int, float)):
            raise ValueError(
                f"Invalid mastery score for topic '{topic_id}'"
            )

        if not 0 <= raw_score <= 100:
            raise ValueError(
                f"Mastery score for '{topic_id}' must be between 0 and 100"
            )

        if raw_score >= 60:
            continue

        difficulty = _get_revision_difficulty(raw_score)

        questions = _select_questions(
            course_id=course_id,
            topic_id=topic_id,
            difficulty=difficulty,
            questions_per_topic=questions_per_topic,
        )

        if not questions:
            continue

        revision_topics.append({
            "topic_id": topic_id,
            "mastery_score": raw_score,
            "difficulty": difficulty,
            "reason": (
                f"Your mastery in {topic_id} is {raw_score}%. "
                "Revision is recommended to strengthen this topic."
            ),
            "total_questions": len(questions),
            "questions": questions,
        })

    return {
        "learner_id": analysis.get("learner_id"),
        "course_id": course_id,
        "revision_required": bool(revision_topics),
        "total_questions": sum(
            topic["total_questions"] for topic in revision_topics
        ),
        "total_topics": len(revision_topics),
        "revision_topics": revision_topics,
        "message": (
            "Targeted revision quiz generated successfully."
            if revision_topics
            else "No revision required for topics with assessed mastery."
        ),
    }
