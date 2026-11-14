
"""Adapter layer to normalize learner analysis and profile input.

Supports sample analysis, backend database fields, and custom learner
dictionaries with topics, topic_mastery, or mastery data.
"""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class NormalizedLearner:
    """Standardized learner representation."""

    learner_id: str
    daily_minutes: int
    topic_scores: dict[str, float | None]
    course: str | None = None
    goal: str | None = None
    level: str | None = None
    interests: list[str] = field(default_factory=list)


def _validate_daily_minutes(value: Any) -> int:
    """Validate and normalize daily study minutes."""

    if isinstance(value, bool):
        raise ValueError("daily_minutes must be a non-negative integer.")

    if isinstance(value, int):
        minutes = value
    elif isinstance(value, str) and value.strip().isdigit():
        minutes = int(value.strip())
    else:
        raise ValueError("daily_minutes must be a whole number.")

    if minutes < 0:
        raise ValueError("daily_minutes cannot be negative.")

    return minutes


def _validate_score(value: Any, topic_id: str) -> float | None:
    """Validate a topic mastery score."""

    if value is None:
        return None

    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"Invalid mastery score for '{topic_id}'.")

    score = float(value)

    if not 0 <= score <= 100:
        raise ValueError(
            f"Mastery score for '{topic_id}' must be between 0 and 100."
        )

    return score


def _extract_score(value: Any, topic_id: str) -> float | None:
    """Extract score from a number or topic dictionary."""

    if isinstance(value, dict):
        score = value.get("score")

        if score is None:
            score = value.get("mastery_score")

        return _validate_score(score, topic_id)

    return _validate_score(value, topic_id)


def _merge_topic_scores(
    data: dict[str, Any],
) -> dict[str, float | None]:
    """Merge topic scores from all supported learner data structures."""

    topic_scores: dict[str, float | None] = {}

    for key in ("topics", "topic_mastery", "mastery"):
        raw_topics = data.get(key)

        if raw_topics is None:
            continue

        if isinstance(raw_topics, dict):
            entries = raw_topics.items()

        elif isinstance(raw_topics, list):
            entries = []

            for item in raw_topics:
                if not isinstance(item, dict):
                    raise ValueError(
                        "Each topic entry must be a dictionary."
                    )

                topic_id = item.get("topic_id") or item.get("topic")

                if not isinstance(topic_id, str) or not topic_id.strip():
                    raise ValueError(
                        "Each topic must have a valid topic_id."
                    )

                entries.append((topic_id, item))

        else:
            raise TypeError(
                f"{key} must be a dictionary or a list."
            )

        for topic_id, value in entries:
            if not isinstance(topic_id, str) or not topic_id.strip():
                raise ValueError("Topic IDs must be non-empty strings.")

            score = _extract_score(value, topic_id)

            # Later sources take priority when they contain a valid score.
            # A None value does not erase an existing valid score.
            if score is not None or topic_id not in topic_scores:
                topic_scores[topic_id] = score

    return topic_scores


def normalize_analysis(data: dict[str, Any]) -> NormalizedLearner:
    """Normalize supported learner-analysis and profile formats."""

    if not isinstance(data, dict):
        raise TypeError("Learner analysis must be a dictionary.")

    learner_id = (
        data.get("learner_id")
        or data.get("user_id")
        or "anonymous_learner"
    )

    if not isinstance(learner_id, str) or not learner_id.strip():
        raise ValueError("learner_id must be a non-empty string.")

    raw_minutes = data.get("daily_minutes")

    if raw_minutes is None:
        raw_minutes = data.get("daily_study_minutes", 60)

    daily_minutes = _validate_daily_minutes(raw_minutes)

    topic_scores = _merge_topic_scores(data)

    course = data.get("course")
    goal = data.get("goal")
    level = data.get("level")
    interests = data.get("interests", [])

    if course is not None and (
        not isinstance(course, str) or not course.strip()
    ):
        raise ValueError("course must be a non-empty string.")

    if goal is not None and (
        not isinstance(goal, str) or not goal.strip()
    ):
        raise ValueError("goal must be a non-empty string.")

    if level is not None:
        if not isinstance(level, str) or level not in (
            "beginner",
            "intermediate",
            "advanced",
        ):
            raise ValueError(
                "level must be beginner, intermediate or advanced."
            )

    if not isinstance(interests, list) or any(
        not isinstance(item, str) or not item.strip()
        for item in interests
    ):
        raise ValueError("interests must be a list of non-empty strings.")

    return NormalizedLearner(
        learner_id=learner_id.strip(),
        daily_minutes=daily_minutes,
        topic_scores=topic_scores,
        course=course.strip() if course else None,
        goal=goal.strip() if goal else None,
        level=level,
        interests=[item.strip() for item in interests],
    )
