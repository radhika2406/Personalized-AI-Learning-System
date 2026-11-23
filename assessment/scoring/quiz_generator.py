
"""
quiz_generator.py

Generates topic-wise and multi-topic quizzes
for all registered courses.
"""

from typing import Dict, List, Optional, Any

from ai_engine.common.course_config import get_course
from assessment.question_management.loader import (
    load_course_topics,
    get_questions_by_topic,
)


def _validate_course(course_id: str) -> Dict[str, Any]:
    """Validate and return course configuration."""
    course = get_course(course_id)

    if not course:
        raise ValueError(f"Unknown course: {course_id}")

    return course


def _validate_question_count(count: int, field_name: str) -> None:
    """Validate a requested question count."""
    if isinstance(count, bool) or not isinstance(count, int) or count < 1:
        raise ValueError(f"{field_name} must be a positive whole number")


def _get_valid_topic_ids(course_id: str) -> set:
    """Get topic IDs belonging to the selected course."""
    topics = load_course_topics(course_id)

    return {
        topic.get("id") or topic.get("topic_id")
        for topic in topics
    }


def generate_topic_quiz(
    course_id: str,
    topic_id: str,
    num_questions: int = 6,
    difficulty: Optional[str] = None
) -> Dict[str, Any]:
    """
    Generate a quiz for one topic in any course.
    """

    course = _validate_course(course_id)
    _validate_question_count(num_questions, "num_questions")

    valid_topic_ids = _get_valid_topic_ids(course_id)

    if topic_id not in valid_topic_ids:
        raise ValueError(
            f"Topic '{topic_id}' does not belong to course '{course_id}'"
        )

    if difficulty is not None:
        difficulty = difficulty.strip().lower()

        if difficulty not in {"easy", "medium", "hard"}:
            raise ValueError(
                "difficulty must be easy, medium, hard or None"
            )

    available_questions = get_questions_by_topic(
        course_id,
        topic_id,
        difficulty=difficulty
    )

    if not available_questions:
        raise ValueError(
            f"No questions available for course '{course_id}', "
            f"topic '{topic_id}'"
        )

    selected_questions = available_questions[:num_questions]

    return {
        "quiz_id": f"{course_id}_{topic_id}_quiz",
        "course_id": course_id,
        "course_name": course["name"],
        "topic_id": topic_id,
        "difficulty": difficulty,
        "total_questions": len(selected_questions),
        "questions": selected_questions,
    }


def generate_multi_topic_quiz(
    course_id: str,
    topic_ids: List[str],
    questions_per_topic: int = 2,
    difficulty: Optional[str] = None
) -> Dict[str, Any]:
    """
    Generate one quiz containing questions from multiple topics
    of the same selected course.
    """

    course = _validate_course(course_id)
    _validate_question_count(
        questions_per_topic,
        "questions_per_topic"
    )

    if not isinstance(topic_ids, list) or not topic_ids:
        raise ValueError("topic_ids must be a non-empty list")

    valid_topic_ids = _get_valid_topic_ids(course_id)

    if len(topic_ids) != len(set(topic_ids)):
        raise ValueError("Duplicate topic IDs are not allowed")

    invalid_topics = [
        topic_id
        for topic_id in topic_ids
        if topic_id not in valid_topic_ids
    ]

    if invalid_topics:
        raise ValueError(
            f"Topics do not belong to course '{course_id}': "
            f"{invalid_topics}"
        )

    if difficulty is not None:
        difficulty = difficulty.strip().lower()

        if difficulty not in {"easy", "medium", "hard"}:
            raise ValueError(
                "difficulty must be easy, medium, hard or None"
            )

    selected_questions = []

    for topic_id in topic_ids:
        available = get_questions_by_topic(
            course_id,
            topic_id,
            difficulty=difficulty
        )

        selected_questions.extend(
            available[:questions_per_topic]
        )

    if not selected_questions:
        raise ValueError(
            f"No questions available for course '{course_id}'"
        )

    return {
        "quiz_id": f"{course_id}_multi_topic_quiz",
        "course_id": course_id,
        "course_name": course["name"],
        "topic_ids": topic_ids,
        "difficulty": difficulty,
        "total_questions": len(selected_questions),
        "questions": selected_questions,
    }
