
"""
initial_assessment.py

Generates and evaluates a 24-question diagnostic assessment
for all registered courses.
"""

import random
from uuid import uuid4
from typing import Dict, Any

from ai_engine.common.course_config import get_course
from ai_engine.common.schemas import mastery_level
from assessment.question_management.loader import (
    load_course_topics,
    load_course_questions,
)
from assessment.scoring.evaluator import evaluate_answers


QUESTIONS_PER_DIFFICULTY = 8
TOTAL_QUESTIONS = 24

DIFFICULTIES = ("easy", "medium", "hard")


def classify_initial_level(score_pct: int) -> str:
    """Classify a learner based on their initial assessment score."""

    if (
        isinstance(score_pct, bool)
        or not isinstance(score_pct, (int, float))
        or not 0 <= score_pct <= 100
    ):
        raise ValueError("score_pct must be a number between 0 and 100")

    if score_pct < 40:
        return "beginner"
    elif score_pct < 80:
        return "intermediate"
    else:
        return "advanced"


def generate_initial_assessment(course_id: str) -> Dict[str, Any]:
    """
    Generate a randomized 24-question initial assessment.

    Covers every topic with:
    - 8 easy questions
    - 8 medium questions
    - 8 hard questions

    Eight topics receive two questions.
    The remaining eight topics receive one question.
    """

    course = get_course(course_id)

    if not course:
        raise ValueError(f"Unknown course: {course_id}")

    topics = load_course_topics(course_id)
    question_bank = load_course_questions(course_id)

    topic_ids = [
        topic.get("id") or topic.get("topic_id")
        for topic in topics
    ]

    if len(topic_ids) != 16 or len(set(topic_ids)) != 16:
        raise ValueError(
            "Initial assessment requires exactly 16 unique course topics"
        )

    # Group questions by topic and difficulty.
    grouped = {
        topic_id: {
            difficulty: []
            for difficulty in DIFFICULTIES
        }
        for topic_id in topic_ids
    }

    for question in question_bank.values():
        topic_id = question.get("topic") or question.get("topic_id")
        difficulty = question.get("difficulty", "").strip().lower()

        if topic_id in grouped and difficulty in DIFFICULTIES:
            grouped[topic_id][difficulty].append(question)

    # Randomize topic distribution.
    shuffled_topics = topic_ids.copy()
    random.shuffle(shuffled_topics)

    easy_topics = shuffled_topics[:8]
    medium_topics = shuffled_topics[8:]

    selected_questions = []

    def select_question(topic_id, difficulty):
        available = grouped[topic_id][difficulty]

        if not available:
            raise ValueError(
                f"No {difficulty} questions available for topic "
                f"'{topic_id}' in course '{course_id}'"
            )

        return random.choice(available)

    # Select one easy or medium question for every topic.
    for topic_id in easy_topics:
        selected_questions.append(
            select_question(topic_id, "easy")
        )

    for topic_id in medium_topics:
        selected_questions.append(
            select_question(topic_id, "medium")
        )

    # Add one hard question to eight randomly selected topics.
    hard_topics = random.sample(topic_ids, 8)

    for topic_id in hard_topics:
        selected_questions.append(
            select_question(topic_id, "hard")
        )

    random.shuffle(selected_questions)

    # Remove correct answers and explanations from learner-facing data.
    public_questions = []

    for question in selected_questions:
        public_question = {
            key: value
            for key, value in question.items()
            if key not in {
                "correct",
                "correct_answer",
                "answer",
                "explanation",
            }
        }
        public_questions.append(public_question)

    return {
        "assessment_id": uuid4().hex,
        "course_id": course_id,
        "course_name": course["name"],
        "total_questions": TOTAL_QUESTIONS,
        "difficulty_distribution": {
            "easy": 8,
            "medium": 8,
            "hard": 8,
        },
        "topic_ids": topic_ids,
        "questions": public_questions,
    }


def evaluate_initial_assessment(
    learner_id: str,
    course_id: str,
    answers: Dict[str, Any],
    assessment: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Evaluate a learner's initial diagnostic assessment.

    Unanswered questions are counted as skipped.
    Returns overall and topic-wise diagnostic results.
    """

    if not isinstance(learner_id, str) or not learner_id.strip():
        raise ValueError("learner_id is required")

    if not get_course(course_id):
        raise ValueError(f"Unknown course: {course_id}")

    if not isinstance(assessment, dict):
        raise ValueError("assessment must be a dictionary")

    if assessment.get("course_id") != course_id:
        raise ValueError("Assessment course does not match course_id")

    questions = assessment.get("questions")

    if not isinstance(questions, list) or len(questions) != TOTAL_QUESTIONS:
        raise ValueError("Assessment must contain exactly 24 questions")

    if not isinstance(answers, dict):
        raise ValueError("answers must be a dictionary")

    question_ids = [
        question.get("question_id")
        for question in questions
        if isinstance(question, dict)
    ]

    if len(question_ids) != TOTAL_QUESTIONS or any(
        not qid for qid in question_ids
    ):
        raise ValueError("Assessment contains invalid question IDs")

    if len(set(question_ids)) != TOTAL_QUESTIONS:
        raise ValueError("Assessment contains duplicate question IDs")

    unknown_answers = set(answers) - set(question_ids)

    if unknown_answers:
        raise ValueError(
            f"Answers contain unknown question IDs: {sorted(unknown_answers)}"
        )

    question_bank = load_course_questions(course_id)

    selected_question_bank = {}

    for question in questions:
        qid = question["question_id"]

        if qid not in question_bank:
            raise ValueError(
                f"Question '{qid}' does not exist in the course question bank"
            )

        original = question_bank[qid]
        topic_id = original.get("topic") or original.get("topic_id")

        if topic_id != question.get("topic") and topic_id != question.get("topic_id"):
            raise ValueError(
                f"Question '{qid}' has an inconsistent topic"
            )

        selected_question_bank[qid] = original

    # Include unanswered questions so the denominator remains 24.
    complete_answers = {
        qid: answers.get(qid)
        for qid in question_ids
    }

    evaluation = evaluate_answers(
        complete_answers,
        selected_question_bank,
    )

    topic_lookup = {
        topic.get("id") or topic.get("topic_id"): topic
        for topic in load_course_topics(course_id)
    }

    topic_results = {}

    for question in questions:
        qid = question["question_id"]
        original = selected_question_bank[qid]
        topic_id = original.get("topic") or original.get("topic_id")

        if topic_id not in topic_results:
            topic_results[topic_id] = {
                "topic_id": topic_id,
                "topic_name": topic_lookup[topic_id].get("title"),
                "correct_count": 0,
                "total_questions": 0,
            }

        topic_results[topic_id]["total_questions"] += 1

    for item in evaluation["breakdown"]:
        qid = item["question_id"]
        original = selected_question_bank[qid]
        topic_id = original.get("topic") or original.get("topic_id")

        if item["is_correct"]:
            topic_results[topic_id]["correct_count"] += 1

    for result in topic_results.values():
        score = round(
            result["correct_count"]
            / result["total_questions"]
            * 100
        )

        result["score_pct"] = score
        result["mastery_level"] = mastery_level(score)

    return {
        "learner_id": learner_id,
        "course_id": course_id,
        "assessment_id": assessment.get("assessment_id"),
        "overall_score_pct": evaluation["score_pct"],
	"initial_level": classify_initial_level(evaluation["score_pct"]),
        "correct_count": evaluation["correct_count"],
        "total_questions": evaluation["total_questions"],
        "wrong_question_ids": evaluation["wrong_question_ids"],
        "breakdown": evaluation["breakdown"],
        "topic_results": topic_results,
    }
