"""
validator.py

Validates syllabi, topic structures, question completeness, option consistency,
and absence of duplicates across all 12 courses.
"""

from typing import Dict, List, Tuple, Any, Optional
from ai_engine.common.course_config import COURSES, list_courses
from assessment.question_management.loader import (
    load_course_syllabus,
    load_course_topics,
    load_course_questions,
)

VALID_DIFFICULTIES = {"easy", "medium", "hard"}
VALID_ANSWER_KEYS = {"a", "b", "c", "d"}
REQUIRED_FIELDS = [
    "question_id", "category", "course", "topic",
    "difficulty", "question", "option_a", "option_b",
    "option_c", "option_d", "correct", "explanation"
]


def validate_question(
    q: Dict[str, Any],
    valid_topics: Optional[List[str]] = None,
    expected_course: Optional[str] = None
) -> List[str]:
    """
    Validate a single question dictionary.
    Returns a list of error message strings (empty list if valid).
    """
    errors = []
    qid = q.get("question_id", "").strip()
    if not qid:
        errors.append("Question is missing question_id.")
        qid = "<unknown>"

    # Check required fields
    for field in REQUIRED_FIELDS:
        val = q.get(field)
        if val is None or str(val).strip() == "":
            errors.append(f"Question {qid}: missing or empty field '{field}'.")

    # Difficulty validation
    diff = str(q.get("difficulty", "")).strip().lower()
    if diff not in VALID_DIFFICULTIES:
        errors.append(f"Question {qid}: invalid difficulty '{diff}'. Must be one of {VALID_DIFFICULTIES}.")

    # Answer key validation
    corr = str(q.get("correct", "")).strip().lower()
    if corr not in VALID_ANSWER_KEYS:
        errors.append(f"Question {qid}: invalid correct key '{corr}'. Must be a, b, c, or d.")

    # Options presence
    for opt in ["option_a", "option_b", "option_c", "option_d"]:
        if not str(q.get(opt, "")).strip():
            errors.append(f"Question {qid}: option '{opt}' is empty.")

    # Course check
    course = q.get("course", "").strip().lower()
    if expected_course and course != expected_course.lower():
        errors.append(f"Question {qid}: course '{course}' does not match expected '{expected_course}'.")

    # Topic check
    topic = q.get("topic") or q.get("topic_id")
    if valid_topics and topic not in valid_topics:
        errors.append(f"Question {qid}: topic '{topic}' is not in valid topics for {expected_course}.")

    return errors


def validate_course(course_id: str) -> Tuple[bool, List[str], Dict[str, Any]]:
    """
    Validate a complete course: syllabus, topics, questions, and difficulty distribution.
    Returns (is_valid, error_list, stats).
    """
    errors: List[str] = []
    stats: Dict[str, Any] = {
        "course_id": course_id,
        "topic_count": 0,
        "question_count": 0,
        "easy_count": 0,
        "medium_count": 0,
        "hard_count": 0,
    }

    if course_id not in COURSES:
        errors.append(f"Unknown course '{course_id}'.")
        return False, errors, stats

    # 1. Load syllabus
    try:
        syllabus = load_course_syllabus(course_id)
        if not syllabus.get("topics"):
            errors.append(f"Course {course_id} syllabus has no topics.")
        if not syllabus.get("checkpoints"):
            errors.append(f"Course {course_id} syllabus missing checkpoints.")
    except Exception as e:
        errors.append(f"Failed to load syllabus for {course_id}: {str(e)}")
        return False, errors, stats

    # 2. Load topics
    try:
        topics = load_course_topics(course_id)
        topic_ids = [t["id"] for t in topics if "id" in t]
        stats["topic_count"] = len(topic_ids)
        if len(topic_ids) == 0:
            errors.append(f"Course {course_id} has no valid topic definitions.")
    except Exception as e:
        errors.append(f"Failed to load topics for {course_id}: {str(e)}")
        return False, errors, stats

    # 3. Load questions
    try:
        questions = load_course_questions(course_id)
        stats["question_count"] = len(questions)
    except Exception as e:
        errors.append(f"Failed to load questions for {course_id}: {str(e)}")
        return False, errors, stats

    # 4. Check each question
    course_qids = set()
    topic_question_counts: Dict[str, Dict[str, int]] = {
        tid: {"easy": 0, "medium": 0, "hard": 0} for tid in topic_ids
    }

    for qid, q in questions.items():
        if qid in course_qids:
            errors.append(f"Duplicate question ID within course {course_id}: {qid}")
        course_qids.add(qid)

        q_errs = validate_question(q, valid_topics=topic_ids, expected_course=course_id)
        errors.extend(q_errs)

        diff = str(q.get("difficulty", "")).strip().lower()
        topic = q.get("topic") or q.get("topic_id")
        if diff == "easy":
            stats["easy_count"] += 1
        elif diff == "medium":
            stats["medium_count"] += 1
        elif diff == "hard":
            stats["hard_count"] += 1

        if topic in topic_question_counts and diff in topic_question_counts[topic]:
            topic_question_counts[topic][diff] += 1

    # 5. Check per-topic distribution
    for tid, counts in topic_question_counts.items():
        if counts["easy"] < 1:
            errors.append(f"Course {course_id}, Topic {tid} has no easy questions.")
        if counts["medium"] < 1:
            errors.append(f"Course {course_id}, Topic {tid} has no medium questions.")
        if counts["hard"] < 1:
            errors.append(f"Course {course_id}, Topic {tid} has no hard questions.")

    is_valid = len(errors) == 0
    return is_valid, errors, stats


def validate_all_courses() -> Tuple[bool, List[str], Dict[str, Any]]:
    """
    Validate all 12 courses, ensuring cross-course uniqueness of question IDs.
    Returns (is_valid, all_errors, aggregated_summary).
    """
    all_errors: List[str] = []
    global_qids = set()
    summary: Dict[str, Any] = {
        "total_courses": 0,
        "valid_courses": 0,
        "total_questions": 0,
        "total_topics": 0,
        "easy_count": 0,
        "medium_count": 0,
        "hard_count": 0,
        "course_stats": {}
    }

    for course_id in list_courses():
        summary["total_courses"] += 1
        is_valid, errs, stats = validate_course(course_id)
        if not is_valid:
            all_errors.extend(errs)
        else:
            summary["valid_courses"] += 1

        summary["total_questions"] += stats["question_count"]
        summary["total_topics"] += stats["topic_count"]
        summary["easy_count"] += stats["easy_count"]
        summary["medium_count"] += stats["medium_count"]
        summary["hard_count"] += stats["hard_count"]
        summary["course_stats"][course_id] = stats

        # Cross-course ID uniqueness
        try:
            questions = load_course_questions(course_id)
            for qid in questions:
                if qid in global_qids:
                    all_errors.append(f"Global duplicate question ID detected: {qid}")
                global_qids.add(qid)
        except Exception:
            pass

    overall_valid = len(all_errors) == 0
    return overall_valid, all_errors, summary
