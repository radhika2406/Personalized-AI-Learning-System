
"""Topic recommender engine.

Recommends study topics according to learner mastery, profile preferences,
and prerequisite requirements.
"""

import csv
from pathlib import Path
from typing import Any

from ai_engine.recommendation.adapter import (
    NormalizedLearner,
    normalize_analysis,
)
from ai_engine.recommendation.config import (
    DEFAULT_TOPICS,
    LEVEL_WEAK,
    LEVEL_DEVELOPING,
    LEVEL_NOT_ASSESSED,
    LEVEL_GOOD,
    LEVEL_STRONG,
    get_mastery_level,
    get_activity_for_level,
)


def _parse_positive_integer(value: Any, field: str, topic_id: str) -> int:
    """Validate and convert a positive integer metadata value."""

    if isinstance(value, bool):
        raise ValueError(f"Invalid {field} for topic '{topic_id}'.")

    try:
        parsed = int(value)
    except (TypeError, ValueError):
        raise ValueError(f"Invalid {field} for topic '{topic_id}'.")

    if str(value).strip() != str(parsed) or parsed <= 0:
        raise ValueError(f"Invalid {field} for topic '{topic_id}'.")

    return parsed


def _split_metadata_values(value: Any) -> list[str]:
    """Convert comma- or semicolon-separated metadata into a list."""

    if isinstance(value, list):
        return [
            item.strip().lower()
            for item in value
            if isinstance(item, str) and item.strip()
        ]

    if not isinstance(value, str) or not value.strip():
        return []

    return [
        item.strip().lower()
        for item in value.replace(",", ";").split(";")
        if item.strip()
    ]


def load_topics_metadata(
    csv_path: str | Path | None = None,
) -> list[dict[str, Any]]:
    """Load and validate topic metadata from topics.csv."""

    if csv_path is None:
        current_dir = Path(__file__).resolve().parent
        csv_path = (
            current_dir.parent.parent
            / "assessment"
            / "content"
            / "topics.csv"
        )

    path = Path(csv_path)

    if not path.is_file():
        topics = [
            {
                "topic_id": topic,
                "course": "python",
                "order": index + 1,
                "prerequisites": [],
                "est_minutes": 20,
            }
            for index, topic in enumerate(DEFAULT_TOPICS)
        ]
        _validate_metadata(topics)
        return topics

    topics = []

    with open(path, mode="r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)

        required_columns = {
            "topic_id",
            "order",
            "prerequisites",
            "est_minutes",
        }

        if not reader.fieldnames or not required_columns.issubset(
            set(reader.fieldnames)
        ):
            raise ValueError(
                "topics.csv must contain topic_id, order, "
                "prerequisites, and est_minutes columns."
            )

        for row in reader:
            topic_id = (row.get("topic_id") or "").strip()

            if not topic_id:
                raise ValueError("Every topic must have a valid topic_id.")

            order = _parse_positive_integer(
                row.get("order"), "order", topic_id
            )
            est_minutes = _parse_positive_integer(
                row.get("est_minutes") or 20,
                "est_minutes",
                topic_id,
            )

            prerequisites_raw = (
                row.get("prerequisites") or ""
            ).strip()

            prerequisites = [
                item.strip()
                for item in prerequisites_raw.split(";")
                if item.strip()
            ]

            topic = {
                "topic_id": topic_id,
                "course": (row.get("course") or "python").strip(),
                "order": order,
                "prerequisites": prerequisites,
                "est_minutes": est_minutes,
            }

            # Preserve optional columns for profile-based personalization.
            for field in (
                "goal",
                "goals",
                "level",
                "difficulty",
                "interests",
                "tags",
                "keywords",
            ):
                value = row.get(field)

                if value is not None:
                    topic[field] = value

            topics.append(topic)

    topics.sort(
        key=lambda topic: (topic["order"], topic["topic_id"])
    )

    _validate_metadata(topics)

    return topics


def _validate_metadata(
    topics_metadata: list[dict[str, Any]],
) -> None:
    """Validate metadata and reject invalid prerequisite dependencies."""

    if not isinstance(topics_metadata, list) or not topics_metadata:
        raise ValueError("Topics metadata must be a non-empty list.")

    topic_ids = []

    for topic in topics_metadata:
        if not isinstance(topic, dict):
            raise ValueError(
                "Each topic metadata entry must be a dictionary."
            )

        topic_id = topic.get("topic_id")

        if not isinstance(topic_id, str) or not topic_id.strip():
            raise ValueError("Every topic must have a valid topic_id.")

        if topic_id != topic_id.strip():
            raise ValueError(
                f"Topic ID '{topic_id}' cannot contain surrounding spaces."
            )

        topic_ids.append(topic_id)

        order = topic.get("order")
        minutes = topic.get("est_minutes")
        prerequisites = topic.get("prerequisites")

        if (
            isinstance(order, bool)
            or not isinstance(order, int)
            or order <= 0
        ):
            raise ValueError(f"Invalid order for topic '{topic_id}'.")

        if (
            isinstance(minutes, bool)
            or not isinstance(minutes, int)
            or minutes <= 0
        ):
            raise ValueError(
                f"Invalid estimated minutes for topic '{topic_id}'."
            )

        if not isinstance(prerequisites, list):
            raise ValueError(
                f"Prerequisites for '{topic_id}' must be a list."
            )

        if any(
            not isinstance(item, str) or not item.strip()
            for item in prerequisites
        ):
            raise ValueError(
                f"Invalid prerequisite entry for topic '{topic_id}'."
            )

        if len(prerequisites) != len(set(prerequisites)):
            raise ValueError(
                f"Duplicate prerequisites found for topic '{topic_id}'."
            )

    if len(topic_ids) != len(set(topic_ids)):
        raise ValueError("Duplicate topic IDs found in metadata.")

    known_topics = set(topic_ids)

    for topic in topics_metadata:
        topic_id = topic["topic_id"]

        for prerequisite in topic["prerequisites"]:
            if prerequisite not in known_topics:
                raise ValueError(
                    f"Unknown prerequisite '{prerequisite}' "
                    f"for topic '{topic_id}'."
                )

            if prerequisite == topic_id:
                raise ValueError(
                    f"Topic '{topic_id}' cannot be its own prerequisite."
                )

    # Detect circular dependencies using topological sorting.
    indegree = {topic_id: 0 for topic_id in topic_ids}
    dependents = {topic_id: [] for topic_id in topic_ids}

    for topic in topics_metadata:
        topic_id = topic["topic_id"]

        for prerequisite in topic["prerequisites"]:
            indegree[topic_id] += 1
            dependents[prerequisite].append(topic_id)

    queue = [
        topic_id
        for topic_id in topic_ids
        if indegree[topic_id] == 0
    ]

    visited = 0

    while queue:
        current = queue.pop(0)
        visited += 1

        for dependent in dependents[current]:
            indegree[dependent] -= 1

            if indegree[dependent] == 0:
                queue.append(dependent)

    if visited != len(topic_ids):
        raise ValueError("Circular prerequisite dependency detected.")


def _urgency_key(
    topic_id: str,
    level: str,
    score: float | None,
    order: int,
) -> tuple[int, float, int, str]:
    """Calculate learning urgency. Lower values mean higher priority."""

    if level == LEVEL_WEAK:
        return (0, score if score is not None else 0.0, order, topic_id)

    if level == LEVEL_DEVELOPING:
        return (1, score if score is not None else 50.0, order, topic_id)

    if level == LEVEL_NOT_ASSESSED:
        return (2, 0.0, order, topic_id)

    if level == LEVEL_GOOD:
        return (3, score if score is not None else 75.0, order, topic_id)

    return (4, score if score is not None else 90.0, order, topic_id)


def _profile_match_score(
    metadata: dict[str, Any],
    learner: NormalizedLearner,
) -> int:
    """Score optional matches between topic metadata and learner profile.

    Profile matching is used only as a tie-breaker between topics with
    similar mastery urgency. Missing metadata does not affect ranking.
    """

    score = 0

    learner_goal = (getattr(learner, "goal", None) or "").strip().lower()
    learner_level = (getattr(learner, "level", None) or "").strip().lower()
    learner_interests = {
        item.strip().lower()
        for item in (getattr(learner, "interests", None) or [])
        if isinstance(item, str) and item.strip()
    }

    topic_goals = set(
        _split_metadata_values(metadata.get("goals"))
        + _split_metadata_values(metadata.get("goal"))
    )

    topic_levels = set(
        _split_metadata_values(metadata.get("level"))
        + _split_metadata_values(metadata.get("difficulty"))
    )

    topic_interests = set(
        _split_metadata_values(metadata.get("interests"))
        + _split_metadata_values(metadata.get("tags"))
        + _split_metadata_values(metadata.get("keywords"))
    )

    if learner_goal and topic_goals:
        if any(
            learner_goal == item
            or learner_goal in item
            or item in learner_goal
            for item in topic_goals
        ):
            score += 3

    if learner_level and topic_levels:
        if learner_level in topic_levels:
            score += 2

    if learner_interests and topic_interests:
        if learner_interests.intersection(topic_interests):
            score += 1

    return score


def _build_reason(
    level: str,
    score: float | None,
    prerequisites: list[str],
    topic_info: dict[str, dict[str, Any]],
    profile_match: int = 0,
) -> str:
    """Generate a deterministic reason using learner and prerequisite data."""

    if level == LEVEL_NOT_ASSESSED or score is None:
        reason = (
            "This topic has not been assessed yet, "
            "so an initial assessment is needed."
        )

    elif level == LEVEL_WEAK:
        reason = (
            f"Mastery is {score:g}%, indicating that this topic "
            "needs focused relearning."
        )

    elif level == LEVEL_DEVELOPING:
        reason = (
            f"Mastery is {score:g}%, indicating that this topic "
            "needs revision to strengthen understanding."
        )

    elif level == LEVEL_GOOD:
        reason = (
            f"Mastery is {score:g}%, so targeted practice can help "
            "strengthen understanding."
        )

    elif level == LEVEL_STRONG:
        reason = (
            f"Mastery is {score:g}%, indicating readiness for "
            "more advanced exercises."
        )

    else:
        raise ValueError(f"Unsupported mastery level: {level}")

    unmastered_prerequisites = [
        prerequisite
        for prerequisite in prerequisites
        if not topic_info[prerequisite]["is_mastered"]
    ]

    if unmastered_prerequisites:
        prerequisite_names = ", ".join(unmastered_prerequisites)
        reason += (
            f" Complete prerequisite topic(s) "
            f"{prerequisite_names} first."
        )

    if profile_match:
        reason += " This topic also matches your learning profile."

    return reason


def recommend_topics(
    analysis: dict[str, Any] | NormalizedLearner,
    topics_metadata: list[dict[str, Any]] | None = None,
) -> list[dict[str, Any]]:
    """Return ordered topic recommendations.

    Each recommendation contains:
        topic_id
        activity
        estimated_minutes
        reason
    """

    if isinstance(analysis, NormalizedLearner):
        normalized = analysis
    else:
        normalized = normalize_analysis(analysis)

    if topics_metadata is None:
        topics_metadata = load_topics_metadata()

    if not isinstance(topics_metadata, list) or not topics_metadata:
        raise ValueError("Topics metadata must be a non-empty list.")

    # Filter by the learner's selected course before validating dependencies.
    learner_course = getattr(normalized, "course", None)

    if learner_course:
        selected_course = learner_course.strip().lower()

        topics_metadata = [
            topic
            for topic in topics_metadata
            if str(topic.get("course") or "python").strip().lower()
            == selected_course
        ]

        if not topics_metadata:
            raise ValueError(
                f"No topics found for course '{learner_course}'."
            )

    _validate_metadata(topics_metadata)

    metadata_map = {
        topic["topic_id"]: topic
        for topic in topics_metadata
    }

    ordered_metadata = sorted(
        topics_metadata,
        key=lambda item: (item["order"], item["topic_id"]),
    )

    all_topic_ids = [
        topic["topic_id"]
        for topic in ordered_metadata
    ]

    topic_info = {}

    for topic_id in all_topic_ids:
        metadata = metadata_map[topic_id]

        score = normalized.topic_scores.get(topic_id)
        level = get_mastery_level(score)
        activity = get_activity_for_level(level)
        profile_match = _profile_match_score(metadata, normalized)

        topic_info[topic_id] = {
            "topic_id": topic_id,
            "score": score,
            "level": level,
            "activity": activity,
            "order": metadata["order"],
            "prerequisites": metadata["prerequisites"],
            "estimated_minutes": metadata["est_minutes"],
            "is_mastered": level in (LEVEL_GOOD, LEVEL_STRONG),
            "profile_match": profile_match,
        }

    scheduled = []
    remaining = set(all_topic_ids)

    # Schedule topics only after their unmastered prerequisites.
    while remaining:
        eligible = []

        for topic_id in remaining:
            info = topic_info[topic_id]

            unmastered_prerequisites = [
                prerequisite
                for prerequisite in info["prerequisites"]
                if not topic_info[prerequisite]["is_mastered"]
            ]

            if all(
                prerequisite in scheduled
                for prerequisite in unmastered_prerequisites
            ):
                eligible.append(topic_id)

        if not eligible:
            raise ValueError(
                "Unable to schedule topics. "
                "Check prerequisite dependencies."
            )

        best_topic = min(
            eligible,
            key=lambda topic_id: (
                _urgency_key(
                    topic_id,
                    topic_info[topic_id]["level"],
                    topic_info[topic_id]["score"],
                    topic_info[topic_id]["order"],
                )[0],
                _urgency_key(
                    topic_id,
                    topic_info[topic_id]["level"],
                    topic_info[topic_id]["score"],
                    topic_info[topic_id]["order"],
                )[1],
                -topic_info[topic_id]["profile_match"],
                topic_info[topic_id]["order"],
                topic_id,
            ),
        )

        scheduled.append(best_topic)
        remaining.remove(best_topic)

    recommendations = []

    for topic_id in scheduled:
        info = topic_info[topic_id]

        recommendations.append({
            "topic_id": topic_id,
            "activity": info["activity"],
            "estimated_minutes": info["estimated_minutes"],
            "reason": _build_reason(
                info["level"],
                info["score"],
                info["prerequisites"],
                topic_info,
                info["profile_match"],
            ),
        })

    return recommendations
