
import pytest

from ai_engine.learner_analysis.analysis_pipeline import analyze_learner


def sample_results():
    return [
        {
            "learner_id": "S101",
            "course": "python",
            "topic": "loops",
            "score_pct": 33,
            "correct": 2,
            "total": 6,
            "attempt": 1
        },
        {
            "learner_id": "S101",
            "course": "python",
            "topic": "variables",
            "score_pct": 83,
            "correct": 5,
            "total": 6,
            "attempt": 1
        }
    ]


def test_complete_learner_analysis():
    result = analyze_learner(sample_results(), "python")

    assert result["learner_id"] == "S101"
    assert result["course"] == "python"
    assert result["mastery"]["loops"] == 33
    assert result["mastery"]["variables"] == 83

def test_weak_and_strong_topics():
    result = analyze_learner(sample_results(), "python")

    assert "loops" in result["weak_topics"]
    assert "variables" in result["strong_topics"]


def test_not_assessed_topics():
    result = analyze_learner(sample_results(), "python")

    assert "functions" in result["not_assessed"]


def test_performance_analysis():
    result = analyze_learner(sample_results(), "python")
    performance = result["performance"]

    assert performance["total_quizzes"] == 2
    assert performance["total_correct"] == 7
    assert performance["total_incorrect"] == 5
    assert performance["average_score"] == 58


def test_empty_quiz_results():
    with pytest.raises(ValueError):
        analyze_learner([], "python")


def test_invalid_quiz_results():
    with pytest.raises(ValueError):
        analyze_learner("invalid", "python")


def test_overall_accuracy():
    result = analyze_learner(sample_results(), "python")

    assert result["performance"]["overall_accuracy"] == 58.33


def test_inconsistent_score_is_rejected():
    results = [{
        "learner_id": "S101",
        "course": "python",
        "topic": "loops",
        "score_pct": 90,
        "correct": 2,
        "total": 6,
        "attempt": 1
    }]

    with pytest.raises(ValueError):
        analyze_learner(results, "python")


def test_boolean_score_is_rejected():
    results = [{
        "learner_id": "S101",
        "course": "python",
        "topic": "loops",
        "score_pct": True,
        "correct": 2,
        "total": 6,
        "attempt": 1
    }]

    with pytest.raises(ValueError):
        analyze_learner(results, "python")


def test_invalid_total_is_rejected():
    results = [{
        "learner_id": "S101",
        "course": "python",
        "topic": "loops",
        "score_pct": 0,
        "correct": 0,
        "total": 0,
        "attempt": 1
    }]

    with pytest.raises(ValueError):
        analyze_learner(results, "python")


def test_score_trend_and_improvement():
    results = [
        {
            "learner_id": "S101",
            "course": "python",
            "topic": "loops",
            "score_pct": 40,
            "correct": 2,
            "total": 5,
            "attempt": 1
        },
        {
            "learner_id": "S101",
            "course": "python",
            "topic": "loops",
            "score_pct": 80,
            "correct": 4,
            "total": 5,
            "attempt": 2
        }
    ]

    result = analyze_learner(results, "python")
    performance = result["performance"]

    assert performance["score_trend"] == [40, 80]
    assert performance["improvement"] == 40
