
"""
Tests for the complete diagnostic assessment workflow.
"""

from ai_engine.learner_analysis.diagnostic_workflow import (
    start_diagnostic_assessment,
    submit_diagnostic_assessment,
)


def test_start_diagnostic_assessment():
    assessment = start_diagnostic_assessment("python")

    assert assessment["course_id"] == "python"
    assert assessment["total_questions"] == 24
    assert len(assessment["questions"]) == 24
    assert assessment["difficulty_distribution"] == {
        "easy": 8,
        "medium": 8,
        "hard": 8,
    }


def test_submit_diagnostic_assessment():
    assessment = start_diagnostic_assessment("python")

    result = submit_diagnostic_assessment(
        learner_id="TEST001",
        course_id="python",
        answers={},
        assessment=assessment,
    )

    assessment_result = result["assessment_result"]
    report = result["diagnostic_report"]

    assert assessment_result["learner_id"] == "TEST001"
    assert assessment_result["overall_score_pct"] == 0
    assert assessment_result["initial_level"] == "beginner"

    assert report["learner_id"] == "TEST001"
    assert report["course_id"] == "python"
    assert report["weak_topics"]
    assert len(report["topic_results"]) == 0 if "topic_results" in report else True


def test_partial_answers():
    assessment = start_diagnostic_assessment("python")

    first_question = assessment["questions"][0]

    result = submit_diagnostic_assessment(
        learner_id="TEST002",
        course_id="python",
        answers={
            first_question["question_id"]: None,
        },
        assessment=assessment,
    )

    assert result["assessment_result"]["total_questions"] == 24
    assert result["assessment_result"]["correct_count"] == 0


def test_invalid_course():
    import pytest

    with pytest.raises(ValueError):
        start_diagnostic_assessment("invalid_course")


def test_mismatched_course_on_submission():
    import pytest

    assessment = start_diagnostic_assessment("python")

    with pytest.raises(ValueError):
        submit_diagnostic_assessment(
            learner_id="TEST003",
            course_id="java",
            answers={},
            assessment=assessment,
        )
