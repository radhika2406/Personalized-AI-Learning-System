"""
evaluator.py

Evaluates quiz and examination answer sheets against question banks,
producing structured scoring reports and wrong question breakdowns.
"""

from typing import Dict, List, Any, Optional
from ai_engine.common.schemas import ANSWER_CHOICES


def evaluate_answers(
    answers: Dict[str, Any],
    questions: Dict[str, Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Evaluate submitted answers against the provided questions dictionary.

    Parameters:
    - answers: mapping of question_id -> chosen option ('a', 'b', 'c', 'd' or empty/None)
    - questions: mapping of question_id -> question details dictionary

    Returns:
    Dict with:
    - score_pct: int percentage (0 to 100)
    - correct_count: int
    - total_questions: int
    - wrong_question_ids: list of question IDs answered incorrectly or skipped
    - breakdown: list of per-question evaluation dicts
    """
    if not answers:
        raise ValueError("No answers submitted for evaluation.")

    correct_count = 0
    wrong_question_ids: List[str] = []
    breakdown: List[Dict[str, Any]] = []

    for qid, chosen in answers.items():
        question = questions.get(qid)
        if question is None:
            raise ValueError(f"Question ID '{qid}' not found in question bank.")

        # Skipped question handling
        if chosen is None or str(chosen).strip() == "":
            wrong_question_ids.append(qid)
            breakdown.append({
                "question_id": qid,
                "chosen": None,
                "correct": question.get("correct", "").strip().lower(),
                "is_correct": False,
                "is_skipped": True,
                "explanation": question.get("explanation", "")
            })
            continue

        chosen_clean = str(chosen).strip().lower()
        if chosen_clean not in ANSWER_CHOICES:
            raise ValueError(f"Invalid answer choice '{chosen}' for question '{qid}'. Must be a, b, c, or d.")

        expected = str(question.get("correct", "")).strip().lower()
        is_correct = (chosen_clean == expected)

        if is_correct:
            correct_count += 1
        else:
            wrong_question_ids.append(qid)

        breakdown.append({
            "question_id": qid,
            "chosen": chosen_clean,
            "correct": expected,
            "is_correct": is_correct,
            "is_skipped": False,
            "explanation": question.get("explanation", "")
        })

    total = len(answers)
    score_pct = round((correct_count / total) * 100) if total > 0 else 0

    return {
        "score_pct": score_pct,
        "correct_count": correct_count,
        "total_questions": total,
        "wrong_question_ids": wrong_question_ids,
        "breakdown": breakdown
    }
