"""
score_quiz.py  (Person A)

Marks a learner's quiz and returns the 'quiz result' (contract 1).

Answers format (agree this with Members 1 and 2):
    {"loops_q1": "b", "loops_q2": "a"}
A skipped question can be sent as "" or None; it counts as wrong.
"""

import csv
from pathlib import Path

from ai_engine.common.schemas import ANSWER_CHOICES, COURSE, TOPICS

DEFAULT_QUESTIONS_PATH = (
    Path(__file__).resolve().parent.parent / "question_bank" / "python_questions.csv"
)


def load_questions(path=DEFAULT_QUESTIONS_PATH):
    """Read the question bank CSV into a dict: {question_id: row_dict}."""
    with open(path, newline="", encoding="utf-8") as f:
        return {row["question_id"]: row for row in csv.DictReader(f)}


def score_quiz(learner_id, topic, answers, questions, attempt=1):
    """Mark one quiz and return the quiz-result dictionary (contract 1)."""
    if not isinstance(learner_id, str) or not learner_id.strip():
        raise ValueError("learner_id is missing")
    if topic not in TOPICS:
        raise ValueError(f"Unknown topic: {topic}")
    if not answers:
        raise ValueError("No answers submitted")
    if isinstance(attempt, bool) or not isinstance(attempt, int) or attempt < 1:
        raise ValueError("attempt must be a whole number of 1 or more")

    correct = 0
    wrong = []
    for question_id, chosen in answers.items():
        question = questions.get(question_id)
        if question is None or question["topic_id"] != topic:
            raise ValueError(f"Unknown question for this topic: {question_id}")

        if chosen is None or str(chosen).strip() == "":
            wrong.append(question_id)  # skipped question counts as wrong
            continue

        letter = str(chosen).strip().lower()
        if letter not in ANSWER_CHOICES:
            raise ValueError(f"Answer for {question_id} must be a, b, c or d")

        if letter == question["correct"].strip().lower():
            correct += 1
        else:
            wrong.append(question_id)

    total = len(answers)
    return {
        "learner_id": learner_id,
        "course": COURSE,
        "topic": topic,
        "score_pct": round(correct / total * 100),
        "correct": correct,
        "total": total,
        "attempt": attempt,
        "wrong_question_ids": wrong,
    }
