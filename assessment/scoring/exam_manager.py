"""
exam_manager.py

Manages the Three-Stage Examination System:
- Stage 1 (Easy Examination): Unlocks after first 10 topics.
- Stage 2 (Medium Examination): Unlocks after next 5 topics (15 total).
- Stage 3 (Hard Examination): Unlocks after remaining topics (16 total).
Enforces strict progression (no skipping stages) and records attempt results.
"""

from typing import Dict, List, Optional, Any
from ai_engine.common.course_config import get_course, get_course_checkpoints
from assessment.question_bank.loader import (
    load_course_topics,
    load_course_questions,
    load_course_syllabus,
)
from assessment.scoring.evaluator import evaluate_answers

STAGE_1 = "stage_1_easy"
STAGE_2 = "stage_2_medium"
STAGE_3 = "stage_3_hard"

STAGE_METADATA = {
    STAGE_1: {
        "name": "Stage 1: Easy Examination",
        "difficulty": "easy",
        "checkpoint_key": "stage_1_easy_exam",
        "default_topics_required": 10,
        "previous_stage": None,
        "description": "Evaluates the student's basic understanding across foundational topics."
    },
    STAGE_2: {
        "name": "Stage 2: Medium Examination",
        "difficulty": "medium",
        "checkpoint_key": "stage_2_medium_exam",
        "default_topics_required": 15,
        "previous_stage": STAGE_1,
        "description": "Evaluates conceptual understanding and practical application."
    },
    STAGE_3: {
        "name": "Stage 3: Hard Examination",
        "difficulty": "hard",
        "checkpoint_key": "stage_3_hard_exam",
        "default_topics_required": 16,
        "previous_stage": STAGE_2,
        "description": "Evaluates advanced understanding, edge cases, and problem-solving ability."
    }
}


def get_checkpoints_for_course(course_id: str) -> Dict[str, int]:
    """Retrieve checkpoints from course syllabus or configuration."""
    try:
        syllabus = load_course_syllabus(course_id)
        if "checkpoints" in syllabus:
            return syllabus["checkpoints"]
    except Exception:
        pass
    return get_course_checkpoints(course_id)


def is_stage_unlocked(
    course_id: str,
    stage: str,
    completed_topic_ids: List[str],
    exam_history: Optional[List[Dict[str, Any]]] = None
) -> Dict[str, Any]:
    """
    Check if a specific examination stage is unlocked for a student.

    Returns:
    Dict with:
    - 'unlocked': bool
    - 'stage': str
    - 'reason': explanation str
    - 'topics_completed': int
    - 'topics_required': int
    """
    if stage not in STAGE_METADATA:
        raise ValueError(f"Unknown exam stage '{stage}'. Valid stages: {list(STAGE_METADATA.keys())}")

    meta = STAGE_METADATA[stage]
    checkpoints = get_checkpoints_for_course(course_id)
    required_count = checkpoints.get(meta["checkpoint_key"], meta["default_topics_required"])

    completed_count = len(completed_topic_ids)
    exam_history = exam_history or []

    # 1. Check prerequisite stage completion (Anti-Skipping Rule)
    prev_stage = meta["previous_stage"]
    if prev_stage is not None:
        prev_passed = any(
            attempt.get("stage") == prev_stage and attempt.get("completion_status") == "passed"
            for attempt in exam_history
        )
        if not prev_passed:
            prev_name = STAGE_METADATA[prev_stage]["name"]
            return {
                "unlocked": False,
                "stage": stage,
                "reason": f"Prerequisite {prev_name} must be passed before unlocking {meta['name']}.",
                "topics_completed": completed_count,
                "topics_required": required_count
            }

    # 2. Check topic progress checkpoint
    if completed_count < required_count:
        return {
            "unlocked": False,
            "stage": stage,
            "reason": f"Requires completing at least {required_count} topics (current: {completed_count}).",
            "topics_completed": completed_count,
            "topics_required": required_count
        }

    return {
        "unlocked": True,
        "stage": stage,
        "reason": f"{meta['name']} is unlocked.",
        "topics_completed": completed_count,
        "topics_required": required_count
    }


def generate_stage_exam(
    course_id: str,
    stage: str,
    completed_topic_ids: List[str],
    exam_history: Optional[List[Dict[str, Any]]] = None,
    num_questions: Optional[int] = None
) -> Dict[str, Any]:
    """
    Generate an examination paper for the specified stage if unlocked.
    Raises ValueError if locked or prerequisite stage was skipped.
    """
    unlock_status = is_stage_unlocked(course_id, stage, completed_topic_ids, exam_history)
    if not unlock_status["unlocked"]:
        raise ValueError(f"Cannot generate examination: {unlock_status['reason']}")

    meta = STAGE_METADATA[stage]
    target_difficulty = meta["difficulty"]

    # Load course topics and questions
    topics = load_course_topics(course_id)
    all_questions = load_course_questions(course_id)

    # Sort topics by order
    sorted_topics = sorted(topics, key=lambda t: t.get("order", 0))
    checkpoints = get_checkpoints_for_course(course_id)
    required_count = checkpoints.get(meta["checkpoint_key"], meta["default_topics_required"])
    eligible_topics = sorted_topics[:required_count]
    eligible_topic_ids = {t["id"] for t in eligible_topics}

    # Gather matching questions of stage difficulty from eligible topics
    stage_questions = []
    for q in all_questions.values():
        q_topic = q.get("topic") or q.get("topic_id")
        q_diff = q.get("difficulty", "").strip().lower()
        if q_topic in eligible_topic_ids and q_diff == target_difficulty:
            stage_questions.append(q)

    # If question count specified, limit
    if num_questions and num_questions > 0:
        selected_questions = stage_questions[:num_questions]
    else:
        selected_questions = stage_questions

    return {
        "exam_title": f"{get_course(course_id)['name']} - {meta['name']}",
        "course_id": course_id,
        "stage": stage,
        "difficulty": target_difficulty,
        "total_questions": len(selected_questions),
        "questions": selected_questions
    }


def record_exam_attempt(
    learner_id: str,
    course_id: str,
    stage: str,
    answers: Dict[str, Any],
    questions: Dict[str, Dict[str, Any]],
    attempt_number: int = 1,
    passing_score: int = 60
) -> Dict[str, Any]:
    """
    Evaluate submitted answers and return a permanent examination record.

    Stored fields:
    - Questions
    - Answers
    - Score
    - Difficulty
    - Attempt number
    - Completion status ('passed' or 'failed')
    """
    if not learner_id or not str(learner_id).strip():
        raise ValueError("learner_id is required.")
    if stage not in STAGE_METADATA:
        raise ValueError(f"Invalid exam stage: {stage}")
    if attempt_number < 1:
        raise ValueError("attempt_number must be 1 or greater.")

    # Evaluate using the evaluator
    eval_result = evaluate_answers(answers, questions)
    score_pct = eval_result["score_pct"]
    completion_status = "passed" if score_pct >= passing_score else "failed"
    difficulty = STAGE_METADATA[stage]["difficulty"]

    return {
        "exam_id": f"{learner_id}_{course_id}_{stage}_att_{attempt_number}",
        "learner_id": learner_id,
        "course_id": course_id,
        "stage": stage,
        "difficulty": difficulty,
        "attempt_number": attempt_number,
        "passing_score": passing_score,
        "score": score_pct,
        "completion_status": completion_status,
        "correct_count": eval_result["correct_count"],
        "total_questions": eval_result["total_questions"],
        "wrong_question_ids": eval_result["wrong_question_ids"],
        "questions": [q.get("question_id") if isinstance(q, dict) else q for q in questions.values()],
        "answers": answers,
        "details": eval_result["breakdown"]
    }
