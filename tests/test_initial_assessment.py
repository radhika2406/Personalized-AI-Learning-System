
"""
Tests for the initial diagnostic assessment.
"""

import pytest

from ai_engine.common.course_config import COURSES
from assessment.question_management.loader import load_course_questions
from assessment.scoring.initial_assessment import (
    generate_initial_assessment,
    evaluate_initial_assessment,
)


@pytest.mark.parametrize("course_id", list(COURSES.keys()))
def test_generate_initial_assessment_for_all_courses(course_id):
    assessment = generate_initial_assessment(course_id)

    assert assessment["course_id"] == course_id
    assert assessment["total_questions"] == 24
    assert len(assessment["questions"]) == 24


@pytest.mark.parametrize("course_id", list(COURSES.keys()))
def test_difficulty_distribution(course_id):
    assessment = generate_initial_assessment(course_id)

    distribution = {}

    for question in assessment["questions"]:
        difficulty = question["difficulty"]
        distribution[difficulty] = distribution.get(difficulty, 0) + 1

    assert distribution == {
        "easy": 8,
        "medium": 8,
        "hard": 8,
    }


@pytest.mark.parametrize("course_id", list(COURSES.keys()))
def test_all_topics_are_covered(course_id):
    assessment = generate_initial_assessment(course_id)

    topic_counts = {}

    for question in assessment["questions"]:
        topic_id = question.get("topic") or question.get("topic_id")
        topic_counts[topic_id] = topic_counts.get(topic_id, 0) + 1

    assert len(topic_counts) == 16
    assert sorted(topic_counts.values()) == [1] * 8 + [2] * 8


def test_correct_answers_are_not_exposed():
    assessment = generate_initial_assessment("python")

    for question in assessment["questions"]:
        assert "correct" not in question
        assert "correct_answer" not in question
        assert "answer" not in question
        assert "explanation" not in question


def test_generate_assessment_has_unique_question_ids():
    assessment = generate_initial_assessment("python")

    question_ids = [
        question["question_id"]
        for question in assessment["questions"]
    ]

    assert len(question_ids) == len(set(question_ids))


def test_evaluate_all_correct_answers():
    course_id = "python"
    assessment = generate_initial_assessment(course_id)
    question_bank = load_course_questions(course_id)

    answers = {
        question["question_id"]: question_bank[
            question["question_id"]
        ]["correct"]
        for question in assessment["questions"]
    }

    result = evaluate_initial_assessment(
        learner_id="TEST001",
        course_id=course_id,
        answers=answers,
        assessment=assessment,
    )

    assert result["learner_id"] == "TEST001"
    assert result["course_id"] == course_id
    assert result["overall_score_pct"] == 100
    assert result["correct_count"] == 24
    assert result["total_questions"] == 24
    assert len(result["topic_results"]) == 16


def test_evaluate_all_wrong_answers():
    course_id = "python"
    assessment = generate_initial_assessment(course_id)

    answers = {
        question["question_id"]: "invalid"
        for question in assessment["questions"]
    }

    # Use a valid but incorrect option for every question.
    question_bank = load_course_questions(course_id)

    for question in assessment["questions"]:
        qid = question["question_id"]
        correct = question_bank[qid]["correct"].strip().lower()
        answers[qid] = "a" if correct != "a" else "b"

    result = evaluate_initial_assessment(
        "TEST002",
        course_id,
        answers,
        assessment,
    )

    assert result["overall_score_pct"] == 0
    assert result["correct_count"] == 0
    assert len(result["wrong_question_ids"]) == 24


def test_skipped_answers_are_counted():
    course_id = "python"
    assessment = generate_initial_assessment(course_id)

    result = evaluate_initial_assessment(
        "TEST003",
        course_id,
        {},
        assessment,
    )

    assert result["total_questions"] == 24
    assert result["correct_count"] == 0
    assert result["overall_score_pct"] == 0
    assert len(result["wrong_question_ids"]) == 24


def test_partial_answers_are_supported():
    course_id = "python"
    assessment = generate_initial_assessment(course_id)
    question_bank = load_course_questions(course_id)

    first_question = assessment["questions"][0]
    qid = first_question["question_id"]

    answers = {
        qid: question_bank[qid]["correct"]
    }

    result = evaluate_initial_assessment(
        "TEST004",
        course_id,
        answers,
        assessment,
    )

    assert result["total_questions"] == 24
    assert result["correct_count"] == 1
    assert result["overall_score_pct"] == round(100 / 24)


def test_invalid_course_is_rejected():
    with pytest.raises(ValueError):
        generate_initial_assessment("invalid_course")


def test_invalid_learner_id_is_rejected():
    assessment = generate_initial_assessment("python")

    with pytest.raises(ValueError):
        evaluate_initial_assessment(
            "",
            "python",
            {},
            assessment,
        )


def test_mismatched_course_is_rejected():
    assessment = generate_initial_assessment("python")

    with pytest.raises(ValueError):
        evaluate_initial_assessment(
            "TEST005",
            "java",
            {},
            assessment,
        )


def test_unknown_question_id_is_rejected():
    assessment = generate_initial_assessment("python")

    with pytest.raises(ValueError):
        evaluate_initial_assessment(
            "TEST006",
            "python",
            {"UNKNOWN_QUESTION": "a"},
            assessment,
        )


from assessment.scoring.initial_assessment import classify_initial_level


@pytest.mark.parametrize(
    "score, expected",
    [
        (0, "beginner"),
        (20, "beginner"),
        (39, "beginner"),
        (40, "intermediate"),
        (60, "intermediate"),
        (79, "intermediate"),
        (80, "advanced"),
        (90, "advanced"),
        (100, "advanced"),
    ],
)
def test_initial_level_classification(score, expected):
    assert classify_initial_level(score) == expected


@pytest.mark.parametrize("score", [-1, 101, "80", None, True])
def test_invalid_initial_level_score(score):
    with pytest.raises(ValueError):
        classify_initial_level(score)
