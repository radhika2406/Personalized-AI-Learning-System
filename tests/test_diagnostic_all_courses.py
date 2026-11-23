
import pytest

from ai_engine.learner_analysis.diagnostic_workflow import (
    start_diagnostic_assessment,
    submit_diagnostic_assessment,
)


COURSES = [
    "python",
    "java",
    "cpp",
    "dsa",
    "machine_learning",
    "deep_learning",
    "data_science",
    "neural_networks",
    "dbms",
    "operating_systems",
    "computer_networks",
    "oop",
]


@pytest.mark.parametrize("course_id", COURSES)
def test_complete_diagnostic_workflow_for_all_courses(course_id):
    # Stage 1: Generate assessment
    assessment = start_diagnostic_assessment(course_id)

    assert assessment["course_id"] == course_id
    assert assessment["total_questions"] == 24
    assert len(assessment["questions"]) == 24

    # Stage 2: Submit an empty answer set
    result = submit_diagnostic_assessment(
        learner_id="TEST001",
        course_id=course_id,
        answers={},
        assessment=assessment,
    )

    assessment_result = result["assessment_result"]
    report = result["diagnostic_report"]

    # Verify evaluation
    assert assessment_result["total_questions"] == 24
    assert assessment_result["correct_count"] == 0
    assert assessment_result["overall_score_pct"] == 0
    assert assessment_result["initial_level"] == "beginner"

    # Verify diagnostic report
    assert report["learner_id"] == "TEST001"
    assert report["course_id"] == course_id
    assert report["total_topics"] == 16
    assert report["assessed_topics"] == 16
    assert len(report["weak_topics"]) == 16
