"""
quiz_generator.py

Generates topic-wise quizzes and practice assessments from the question bank.
"""

from typing import Dict, List, Optional, Any
from ai_engine.common.course_config import get_course
from assessment.question_bank.loader import (
    load_course_questions,
    get_questions_by_topic,
    load_course_topics,
)


def generate_topic_quiz(
    course_id: str,
    topic_id: str,
    num_questions: int = 6,
    difficulty: Optional[str] = None
) -> Dict[str, Any]:
    """
    Generate a quiz for a specific topic in a course.

    Parameters:
    - course_id: course identifier (e.g., 'python', 'java', 'dbms')
    - topic_id: topic identifier (e.g., 'variables', 'indexing_and_hashing')
    - num_questions: target question count (default: 6)
    - difficulty: optional filter ('easy', 'medium', 'hard')

    Returns:
    Dict with quiz details and questions list.
    """
    course = get_course(course_id)
    if not course:
        raise ValueError(f"Unknown course '{course_id}'.")

    # Verify topic belongs to course
    topics = load_course_topics(course_id)
    valid_topic_ids = [t["id"] for t in topics]
    if topic_id not in valid_topic_ids:
        raise ValueError(f"Topic '{topic_id}' does not belong to course '{course_id}'. Valid topics: {valid_topic_ids}")

    # Fetch available questions for this topic
    available = get_questions_by_topic(course_id, topic_id, difficulty=difficulty)
    if not available:
        raise ValueError(f"No questions available for course '{course_id}', topic '{topic_id}'.")

    selected = available[:num_questions]

    return {
        "quiz_id": f"{course_id}_{topic_id}_quiz",
        "course_id": course_id,
        "topic_id": topic_id,
        "total_questions": len(selected),
        "questions": selected
    }


def generate_multi_topic_quiz(
    course_id: str,
    topic_ids: List[str],
    questions_per_topic: int = 2,
    difficulty: Optional[str] = None
) -> Dict[str, Any]:
    """
    Generate a review or diagnostic quiz spanning multiple topics in a course.
    """
    course = get_course(course_id)
    if not course:
        raise ValueError(f"Unknown course '{course_id}'.")

    all_selected = []
    for tid in topic_ids:
        topic_questions = get_questions_by_topic(course_id, tid, difficulty=difficulty)
        all_selected.extend(topic_questions[:questions_per_topic])

    return {
        "quiz_id": f"{course_id}_multi_quiz",
        "course_id": course_id,
        "topics": topic_ids,
        "total_questions": len(all_selected),
        "questions": all_selected
    }
