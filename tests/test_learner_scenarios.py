
import pytest

from ai_engine.learner_analysis.analysis_pipeline import analyze_learner


def create_quiz_result(learner_id, topic, score, correct):
    return {
        "learner_id": learner_id,
        "course": "python",
        "topic": topic,
        "score_pct": score,
        "correct": correct,
        "total": 6,
        "attempt": 1
    }


@pytest.mark.parametrize(
    "learner_id, quiz_results, expected_category, expected_topic",
    [
        (
            "BEGINNER01",
            [create_quiz_result("BEGINNER01", "loops", 33, 2)],
            "weak_topics",
            "loops"
        ),
        (
            "INTERMEDIATE01",
            [create_quiz_result("INTERMEDIATE01", "functions", 50, 3)],
            "developing_topics",
            "functions"
        ),
        (
            "ADVANCED01",
            [create_quiz_result("ADVANCED01", "variables", 100, 6)],
            "strong_topics",
            "variables"
        ),
        (
            "MIXED01",
            [
                create_quiz_result("MIXED01", "loops", 33, 2),
                create_quiz_result("MIXED01", "variables", 100, 6),
                create_quiz_result("MIXED01", "functions", 50, 3)
            ],
            "weak_topics",
            "loops"
        )
    ]
)
def test_different_learner_scenarios(
    learner_id,
    quiz_results,
    expected_category,
    expected_topic
):
    result = analyze_learner(quiz_results, "python")

    assert result["learner_id"] == learner_id
    assert result["course"] == "python"
    assert expected_topic in result[expected_category]


def test_unassessed_topics_for_new_learner():
    results = [
        create_quiz_result("NEW01", "loops", 33, 2)
    ]

    result = analyze_learner(results, "python")

    assert "loops" not in result["not_assessed"]
    assert "variables" in result["not_assessed"]


def test_strong_learner_has_high_average():
    results = [
        create_quiz_result("STRONG01", "variables", 100, 6),
        create_quiz_result("STRONG01", "loops", 100, 6)
    ]

    result = analyze_learner(results, "python")

    assert result["performance"]["average_score"] == 100
    assert len(result["strong_topics"]) == 2
