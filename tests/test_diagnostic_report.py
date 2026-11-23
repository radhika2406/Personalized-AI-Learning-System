
"""
Tests for the diagnostic report generator.
"""

import pytest

from assessment.question_management.loader import load_course_topics
from ai_engine.learner_analysis.diagnostic_report import (
    generate_diagnostic_report,
)


def create_report_input():
    topics = load_course_topics("python")

    topic_ids = [
        topic.get("id") or topic.get("topic_id")
        for topic in topics
    ]

    return {
        "learner_id": "TEST001",
        "course_id": "python",
        "overall_score_pct": 60,
        "initial_level": "intermediate",
        "topic_results": {
            topic_ids[0]: {"score_pct": 20},
            topic_ids[1]: {"score_pct": 50},
            topic_ids[2]: {"score_pct": 70},
            topic_ids[3]: {"score_pct": 90},
        },
    }


def test_generate_diagnostic_report():
    result = generate_diagnostic_report(create_report_input())

    assert result["learner_id"] == "TEST001"
    assert result["course_id"] == "python"
    assert result["overall_score_pct"] == 60
    assert result["initial_level"] == "intermediate"
    assert result["total_topics"] == 16
    assert result["assessed_topics"] == 4


def test_topic_classification():
    data = create_report_input()
    topic_ids = list(data["topic_results"])

    result = generate_diagnostic_report(data)

    assert topic_ids[0] in result["weak_topics"]
    assert topic_ids[1] in result["developing_topics"]
    assert topic_ids[2] in result["good_topics"]
    assert topic_ids[3] in result["strong_topics"]


def test_recommended_starting_topics():
    data = create_report_input()
    topic_ids = list(data["topic_results"])

    result = generate_diagnostic_report(data)

    assert result["recommended_starting_topics"] == [
        topic_ids[0],
        topic_ids[1],
    ]


def test_unassessed_topics_are_used_as_fallback():
    data = create_report_input()
    topic_ids = list(data["topic_results"])

    result = generate_diagnostic_report(data)

    expected = [
        topic.get("id") or topic.get("topic_id")
        for topic in load_course_topics("python")
        if (topic.get("id") or topic.get("topic_id"))
        not in topic_ids
    ]

    # When no weak or developing topics exist, unassessed
    # topics become the recommended starting topics.
    data["topic_results"] = {
        topic_id: {"score_pct": 90}
        for topic_id in topic_ids
    }

    result = generate_diagnostic_report(data)

    assert result["recommended_starting_topics"] == expected


def test_invalid_assessment_result():
    with pytest.raises(ValueError):
        generate_diagnostic_report("invalid")


def test_missing_learner_id():
    data = create_report_input()
    data["learner_id"] = ""

    with pytest.raises(ValueError):
        generate_diagnostic_report(data)


def test_invalid_course():
    data = create_report_input()
    data["course_id"] = "invalid_course"

    with pytest.raises(ValueError):
        generate_diagnostic_report(data)


def test_invalid_overall_score():
    data = create_report_input()
    data["overall_score_pct"] = 120

    with pytest.raises(ValueError):
        generate_diagnostic_report(data)


def test_empty_topic_results():
    data = create_report_input()
    data["topic_results"] = {}

    with pytest.raises(ValueError):
        generate_diagnostic_report(data)


def test_unknown_topic():
    data = create_report_input()
    data["topic_results"] = {
        "unknown_topic": {"score_pct": 50}
    }

    with pytest.raises(ValueError):
        generate_diagnostic_report(data)


def test_invalid_topic_score():
    data = create_report_input()
    topic_id = next(iter(data["topic_results"]))
    data["topic_results"][topic_id]["score_pct"] = 150

    with pytest.raises(ValueError):
        generate_diagnostic_report(data)
