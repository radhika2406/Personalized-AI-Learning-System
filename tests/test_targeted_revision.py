
import pytest

from assessment.scoring import targeted_revision as revision


@pytest.fixture
def mock_course(monkeypatch):
    monkeypatch.setattr(
        revision,
        "get_course",
        lambda course_id: {"id": course_id} if course_id == "python" else None,
    )
    monkeypatch.setattr(
        revision,
        "load_course_topics",
        lambda course_id: [
            {"id": "variables"},
            {"id": "conditions"},
            {"id": "loops"},
            {"id": "functions"},
        ],
    )


def make_questions(topic_id, difficulty, count=5):
    return [
        {
            "question_id": f"{topic_id}_{difficulty}_{i}",
            "topic_id": topic_id,
            "difficulty": difficulty,
            "question": f"Question {i}",
        }
        for i in range(count)
    ]


def test_generates_revision_for_weak_and_developing_topics(
    mock_course, monkeypatch
):
    def fake_questions(course_id, topic_id, difficulty=None):
        return make_questions(topic_id, difficulty)

    monkeypatch.setattr(revision, "get_questions_by_topic", fake_questions)

    result = revision.generate_targeted_revision({
        "learner_id": "learner_01",
        "course": "python",
        "mastery": {
            "variables": 85,
            "conditions": 35,
            "loops": 50,
            "functions": None,
        },
    })

    assert result["revision_required"] is True
    assert result["total_topics"] == 2
    assert result["total_questions"] == 6
    assert [t["topic_id"] for t in result["revision_topics"]] == [
        "conditions",
        "loops",
    ]
    assert result["revision_topics"][0]["difficulty"] == "easy"
    assert result["revision_topics"][1]["difficulty"] == "medium"


def test_score_below_40_uses_easy_difficulty(mock_course, monkeypatch):
    monkeypatch.setattr(
        revision,
        "get_questions_by_topic",
        lambda course, topic, difficulty=None: make_questions(
            topic, difficulty
        ),
    )

    result = revision.generate_targeted_revision({
        "course": "python",
        "mastery": {"variables": 20},
    })

    assert result["revision_topics"][0]["difficulty"] == "easy"


def test_score_40_to_59_uses_medium_difficulty(mock_course, monkeypatch):
    monkeypatch.setattr(
        revision,
        "get_questions_by_topic",
        lambda course, topic, difficulty=None: make_questions(
            topic, difficulty
        ),
    )

    result = revision.generate_targeted_revision({
        "course": "python",
        "mastery": {"variables": 45},
    })

    assert result["revision_topics"][0]["difficulty"] == "medium"


def test_score_60_or_above_does_not_require_revision(
    mock_course, monkeypatch
):
    monkeypatch.setattr(
        revision,
        "get_questions_by_topic",
        lambda *args, **kwargs: pytest.fail(
            "Questions should not be fetched for mastered topics"
        ),
    )

    result = revision.generate_targeted_revision({
        "course": "python",
        "mastery": {
            "variables": 60,
            "conditions": 80,
            "loops": 100,
        },
    })

    assert result["revision_required"] is False
    assert result["total_topics"] == 0
    assert result["total_questions"] == 0
    assert result["revision_topics"] == []


def test_none_mastery_is_skipped(mock_course, monkeypatch):
    monkeypatch.setattr(
        revision,
        "get_questions_by_topic",
        lambda *args, **kwargs: pytest.fail(
            "Questions should not be fetched for unassessed topics"
        ),
    )

    result = revision.generate_targeted_revision({
        "course": "python",
        "mastery": {"variables": None},
    })

    assert result["revision_required"] is False


def test_unknown_topics_are_skipped(mock_course, monkeypatch):
    monkeypatch.setattr(
        revision,
        "get_questions_by_topic",
        lambda *args, **kwargs: pytest.fail(
            "Questions should not be fetched for unknown topics"
        ),
    )

    result = revision.generate_targeted_revision({
        "course": "python",
        "mastery": {"unknown_topic": 20},
    })

    assert result["revision_required"] is False


def test_uses_course_id_alias(mock_course, monkeypatch):
    monkeypatch.setattr(
        revision,
        "get_questions_by_topic",
        lambda course, topic, difficulty=None: make_questions(
            topic, difficulty
        ),
    )

    result = revision.generate_targeted_revision({
        "course_id": "python",
        "mastery": {"variables": 30},
    })

    assert result["course_id"] == "python"
    assert result["revision_required"] is True


def test_uses_fallback_difficulty_when_preferred_is_unavailable(
    mock_course, monkeypatch
):
    requested_levels = []

    def fake_questions(course, topic, difficulty=None):
        requested_levels.append(difficulty)
        if difficulty == "easy":
            return []
        if difficulty == "medium":
            return make_questions(topic, difficulty, count=2)
        return []

    monkeypatch.setattr(
        revision, "get_questions_by_topic", fake_questions
    )

    result = revision.generate_targeted_revision({
        "course": "python",
        "mastery": {"variables": 20},
        })

    assert requested_levels == ["easy", "medium", "hard"]
    assert result["total_questions"] == 2


def test_limits_questions_per_topic(mock_course, monkeypatch):
    monkeypatch.setattr(
        revision,
        "get_questions_by_topic",
        lambda course, topic, difficulty=None: make_questions(
            topic, difficulty, count=10
        ),
    )

    result = revision.generate_targeted_revision({
        "course": "python",
        "mastery": {"variables": 20},
    }, questions_per_topic=2)

    assert result["total_questions"] == 2
    assert result["revision_topics"][0]["total_questions"] == 2


def test_skips_topic_when_no_questions_are_available(
    mock_course, monkeypatch
):
    monkeypatch.setattr(
        revision,
        "get_questions_by_topic",
        lambda *args, **kwargs: [],
    )

    result = revision.generate_targeted_revision({
        "course": "python",
        "mastery": {"variables": 20},
    })

    assert result["revision_required"] is False
    assert result["revision_topics"] == []


@pytest.mark.parametrize("invalid_analysis", [None, [], "python", 123])
def test_rejects_invalid_analysis(invalid_analysis):
    with pytest.raises(ValueError, match="analysis must be a dictionary"):
        revision.generate_targeted_revision(invalid_analysis)


@pytest.mark.parametrize("invalid_count", [0, -1, 1.5, "3", True, None])
def test_rejects_invalid_question_count(invalid_count):
    with pytest.raises(ValueError, match="positive integer"):
        revision.generate_targeted_revision(
            {
                "course": "python",
                "mastery": {},
            },
            questions_per_topic=invalid_count,
        )


def test_rejects_invalid_course(mock_course):
    with pytest.raises(ValueError, match="valid course ID"):
        revision.generate_targeted_revision({
            "course": "unknown",
            "mastery": {},
        })


@pytest.mark.parametrize("invalid_mastery", [None, [], "invalid", 10])
def test_rejects_invalid_mastery(mock_course, invalid_mastery):
    with pytest.raises(ValueError, match="mastery dictionary"):
        revision.generate_targeted_revision({
            "course": "python",
            "mastery": invalid_mastery,
        })


@pytest.mark.parametrize("invalid_score", [-1, 101, "50", True])
def test_rejects_invalid_mastery_scores(mock_course, invalid_score):
    with pytest.raises(ValueError):
        revision.generate_targeted_revision({
            "course": "python",
            "mastery": {"variables": invalid_score},
        })


def test_revision_result_contains_explanation(mock_course, monkeypatch):
    monkeypatch.setattr(
        revision,
        "get_questions_by_topic",
        lambda course, topic, difficulty=None: make_questions(
            topic, difficulty
        ),
    )

    result = revision.generate_targeted_revision({
        "learner_id": "learner_01",
        "course": "python",
        "mastery": {"conditions": 35},
    })

    topic = result["revision_topics"][0]

    assert topic["mastery_score"] == 35
    assert "conditions" in topic["reason"]
    assert "35%" in topic["reason"]
    assert len(topic["questions"]) == topic["total_questions"]
    assert result["learner_id"] == "learner_01"

