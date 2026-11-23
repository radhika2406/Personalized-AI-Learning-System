
import pytest

from assessment.question_management.loader import load_course_topics
from ai_engine.learner_analysis.progress_tracking import (
    build_progress_report,
    COMPLETION_THRESHOLD
)


@pytest.fixture
def topics():
    return load_course_topics("python")


@pytest.fixture
def learner_id():
    return "test_learner"


def make_result(topic, score, learner_id="test_learner", attempt=1):
    correct = round(score * 6 / 100)
    actual_score = round(correct / 6 * 100)

    return {
        "learner_id": learner_id,
        "course": "python",
        "topic": topic,
        "score_pct": actual_score,
        "correct": correct,
        "total": 6,
        "attempt": attempt
    }


def test_new_learner_progress(topics, learner_id):
    report = build_progress_report(
        [],
        "python",
        learner_id=learner_id
    )

    progress = report["course_progress"]

    assert progress["total_topics"] == len(topics)
    assert progress["completed_topics"] == 0
    assert progress["assessed_topics"] == 0
    assert progress["unassessed_topics"] == len(topics)
    assert progress["course_progress_pct"] == 0


def test_topic_completed_at_80_or_above(learner_id):
    results = [
        make_result("variables", 100, learner_id)
    ]

    report = build_progress_report(
        results,
        "python",
        learner_id=learner_id
    )

    topic = report["topic_progress"]["variables"]

    assert topic["status"] == "completed"
    assert topic["score"] == 100
    assert "variables" in report["course_progress"]["completed_topic_ids"]


def test_topic_below_80_is_not_completed(learner_id):
    results = [
        make_result("variables", 50, learner_id)
    ]

    report = build_progress_report(
        results,
        "python",
        learner_id=learner_id
    )

    topic = report["topic_progress"]["variables"]

    assert topic["status"] == "in_progress"
    assert topic["score"] == 50
    assert report["course_progress"]["completed_topics"] == 0


def test_unassessed_topic_remains_unassessed(learner_id):
    report = build_progress_report(
        [],
        "python",
        learner_id=learner_id
    )

    topic = report["topic_progress"]["variables"]

    assert topic["score"] is None
    assert topic["mastery_level"] == "not_assessed"
    assert topic["status"] == "not_assessed"


def test_course_progress_calculation(learner_id):
    results = [
        make_result("variables", 100, learner_id),
        make_result("conditions", 100, learner_id)
    ]

    report = build_progress_report(
        results,
        "python",
        learner_id=learner_id
    )

    progress = report["course_progress"]

    assert progress["completed_topics"] == 2
    assert progress["total_topics"] == 16
    assert progress["course_progress_pct"] == 12.5


def test_multiple_attempts_use_latest_mastery(learner_id):
    results = [
        make_result("variables", 50, learner_id, attempt=1),
        make_result("variables", 100, learner_id, attempt=2)
    ]

    report = build_progress_report(
        results,
        "python",
        learner_id=learner_id
    )

    assert report["topic_progress"]["variables"]["score"] == 100
    assert report["topic_progress"]["variables"]["status"] == "completed"


def test_exam_progress_summary(learner_id):
    exam_history = [
        {
            "learner_id": learner_id,
            "course_id": "python",
            "stage": "stage_1_easy",
            "attempt_number": 1,
            "score": 80,
            "completion_status": "passed"
        },
        {
            "learner_id": learner_id,
            "course_id": "python",
            "stage": "stage_2_medium",
            "attempt_number": 1,
            "score": 45,
            "completion_status": "failed"
        }
    ]

    report = build_progress_report(
        [],
        "python",
        learner_id=learner_id,
        exam_history=exam_history
    )

    exam = report["exam_progress"]

    assert exam["total_stages"] == 3
    assert exam["passed_stages"] == 1
    assert exam["pending_stages"] == 2

    assert exam["stages"][0]["status"] == "passed"
    assert exam["stages"][1]["status"] == "failed"
    assert exam["stages"][2]["status"] == "pending"


def test_other_learner_exam_records_are_ignored(learner_id):
    exam_history = [
        {
            "learner_id": "another_learner",
            "course_id": "python",
            "stage": "stage_1_easy",
            "attempt_number": 1,
            "score": 90,
            "completion_status": "passed"
        }
    ]

    report = build_progress_report(
        [],
        "python",
        learner_id=learner_id,
        exam_history=exam_history
    )

    assert report["exam_progress"]["passed_stages"] == 0


def test_invalid_course_raises_error(learner_id):
    with pytest.raises(ValueError):
        build_progress_report(
            [],
            "unknown_course",
            learner_id=learner_id
        )


def test_invalid_quiz_results_raise_error(learner_id):
    with pytest.raises(ValueError):
        build_progress_report(
            "not a list",
            "python",
            learner_id=learner_id
        )


def test_invalid_exam_history_raises_error(learner_id):
    with pytest.raises(ValueError):
        build_progress_report(
            [],
            "python",
            learner_id=learner_id,
            exam_history="invalid"
        )


def test_completion_threshold_is_80():
    assert COMPLETION_THRESHOLD == 80
