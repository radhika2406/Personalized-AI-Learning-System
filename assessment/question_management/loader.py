"""
loader.py

Loads syllabi, topics, and question banks for all 12 courses.
Normalizes key aliases (e.g., id <-> topic_id, level <-> difficulty_stage)
so client code has uniform, reliable access.
"""

import csv
import json
from pathlib import Path
from typing import Dict, List, Optional, Any

from ai_engine.common.course_config import COURSES, get_course


def _get_course_dir(course_id: str) -> Path:
    """Resolve the directory path for a course."""
    course = get_course(course_id)
    if not course:
        raise ValueError(f"Unknown course '{course_id}'. Valid courses: {list(COURSES.keys())}")
    return Path(course["path"])


def _normalize_topic(topic_dict: Dict[str, Any]) -> Dict[str, Any]:
    """Normalize a topic dictionary with standard alias keys."""
    # ID aliases
    tid = topic_dict.get("id") or topic_dict.get("topic_id")
    if tid:
        topic_dict["id"] = tid
        topic_dict["topic_id"] = tid

    # Title / Name aliases
    title = topic_dict.get("name") or topic_dict.get("title")
    if title:
        topic_dict["name"] = title
        topic_dict["title"] = title

    # Level / Difficulty stage aliases
    stage = (
        topic_dict.get("difficulty_stage")
        or topic_dict.get("level")
        or topic_dict.get("difficulty_level")
    )
    if stage:
        topic_dict["difficulty_stage"] = stage
        topic_dict["level"] = stage
        topic_dict["difficulty_level"] = stage

    return topic_dict


def load_course_syllabus(course_id: str) -> Dict[str, Any]:
    """Load syllabus.json for a given course."""
    course_dir = _get_course_dir(course_id)
    syllabus_path = course_dir / "syllabus.json"
    if not syllabus_path.exists():
        raise FileNotFoundError(f"Syllabus file not found at {syllabus_path}")

    with open(syllabus_path, mode="r", encoding="utf-8") as f:
        data = json.load(f)

    # Normalize topics list in syllabus if present
    if "topics" in data and isinstance(data["topics"], list):
        data["topics"] = [_normalize_topic(t) for t in data["topics"]]

    # Normalize course title / name
    name = data.get("course_name") or data.get("course_title")
    if name:
        data["course_name"] = name
        data["course_title"] = name

    # Normalize checkpoints keys
    if "checkpoints" in data and isinstance(data["checkpoints"], dict):
        cp = data["checkpoints"]
        if "stage_1_easy" in cp and "stage_1_easy_exam" not in cp:
            cp["stage_1_easy_exam"] = cp["stage_1_easy"]
        elif "stage_1_easy_exam" in cp and "stage_1_easy" not in cp:
            cp["stage_1_easy"] = cp["stage_1_easy_exam"]

        if "stage_2_medium" in cp and "stage_2_medium_exam" not in cp:
            cp["stage_2_medium_exam"] = cp["stage_2_medium"]
        elif "stage_2_medium_exam" in cp and "stage_2_medium" not in cp:
            cp["stage_2_medium"] = cp["stage_2_medium_exam"]

        if "stage_3_hard" in cp and "stage_3_hard_exam" not in cp:
            cp["stage_3_hard_exam"] = cp["stage_3_hard"]
        elif "stage_3_hard_exam" in cp and "stage_3_hard" not in cp:
            cp["stage_3_hard"] = cp["stage_3_hard_exam"]

    return data


def load_course_topics(course_id: str) -> List[Dict[str, Any]]:
    """Load topics.json for a given course."""
    course_dir = _get_course_dir(course_id)
    topics_path = course_dir / "topics.json"
    if not topics_path.exists():
        raise FileNotFoundError(f"Topics file not found at {topics_path}")

    with open(topics_path, mode="r", encoding="utf-8") as f:
        topics = json.load(f)

    return [_normalize_topic(t) for t in topics]


def load_course_questions(course_id: str) -> Dict[str, Dict[str, str]]:
    """
    Load questions.csv for a course.
    Returns a dictionary mapping question_id -> question row dictionary.
    Ensures 'topic_id' is aliased to 'topic' for backward compatibility.
    """
    course_dir = _get_course_dir(course_id)
    questions_path = course_dir / "questions.csv"
    if not questions_path.exists():
        raise FileNotFoundError(f"Questions file not found at {questions_path}")

    questions: Dict[str, Dict[str, str]] = {}
    with open(questions_path, mode="r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            qid = row.get("question_id")
            if not qid:
                continue
            # Ensure topic_id is accessible whether column is named topic or topic_id
            if "topic" in row and "topic_id" not in row:
                row["topic_id"] = row["topic"]
            elif "topic_id" in row and "topic" not in row:
                row["topic"] = row["topic_id"]
            questions[qid] = row
    return questions


def load_all_questions() -> Dict[str, Dict[str, str]]:
    """Load all questions across all 12 courses into a single dictionary."""
    all_q: Dict[str, Dict[str, str]] = {}
    for course_id in COURSES:
        course_q = load_course_questions(course_id)
        all_q.update(course_q)
    return all_q


def get_questions_by_topic(
    course_id: str,
    topic_id: str,
    difficulty: Optional[str] = None
) -> List[Dict[str, str]]:
    """Return questions for a specific topic, optionally filtered by difficulty."""
    questions = load_course_questions(course_id)
    matched = []
    diff_lower = difficulty.lower().strip() if difficulty else None

    for q in questions.values():
        if q.get("topic") == topic_id or q.get("topic_id") == topic_id:
            if diff_lower is None or q.get("difficulty", "").lower().strip() == diff_lower:
                matched.append(q)
    return matched


def get_questions_by_difficulty(
    course_id: str,
    difficulty: str
) -> List[Dict[str, str]]:
    """Return all questions for a course with the specified difficulty (easy, medium, hard)."""
    questions = load_course_questions(course_id)
    diff_lower = difficulty.lower().strip()
    return [q for q in questions.values() if q.get("difficulty", "").lower().strip() == diff_lower]
