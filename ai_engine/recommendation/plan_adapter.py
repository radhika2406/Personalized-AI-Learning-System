
"""Adapter between backend database records and AI/frontend formats."""

from typing import Any, Mapping


ACTIVITY_CARD_CONFIG = {
    "relearn": {
        "title": "Relearn Topic",
        "type": "quiz_performance",
        "priority": 4,
        "desc_template": (
            "Focus on relearning fundamental concepts and "
            "retrying practice quizzes."
        ),
    },
    "revise": {
        "title": "Revise Topic",
        "type": "quiz_performance",
        "priority": 3,
        "desc_template": (
            "Review key learning materials and reinforce "
            "core programming patterns."
        ),
    },
    "assess first": {
        "title": "Initial Assessment",
        "type": "learning_progress",
        "priority": 3,
        "desc_template": (
            "Complete an initial quiz to assess your knowledge "
            "in this topic."
        ),
    },
    "practice": {
        "title": "Strengthen Your Learning",
        "type": "quiz_performance",
        "priority": 2,
        "desc_template": (
            "Solve practical programming problems to keep "
            "your skills sharp."
        ),
    },
    "advance": {
        "title": "Advanced Learning",
        "type": "learning_progress",
        "priority": 1,
        "desc_template": (
            "Tackle advanced challenges to expand your mastery."
        ),
    },
}


def from_backend_format(
    learner_profile: dict[str, Any],
    topic_masteries: list[dict[str, Any]] | None = None,
    backend_topic_id_map: Mapping[int, str] | None = None,
) -> dict[str, Any]:
    """Convert backend learner and mastery records into AI input.

    backend_topic_id_map maps database Topic.id -> source_topic_id.
    A mastery record may also provide source_topic_id directly.
    """

    learner_id = str(
        learner_profile.get("user_id")
        or learner_profile.get("id")
        or "learner_01"
    )

    daily_minutes_value = learner_profile.get("daily_study_minutes")
    if daily_minutes_value is None:
        daily_minutes_value = learner_profile.get("daily_minutes")
    if daily_minutes_value is None:
        daily_minutes_value = 60

    daily_minutes = int(daily_minutes_value)

    # Extract course identifier.
    # Use course_code or course, not numeric database course_id.
    course = (
        learner_profile.get("course")
        or learner_profile.get("course_code")
    )

    # Extract learning goal.
    goal = (
        learner_profile.get("learning_goal")
        or learner_profile.get("learning_target")
        or learner_profile.get("goal")
    )

    # Extract current learning level.
    level = (
        learner_profile.get("current_level")
        or learner_profile.get("level")
    )

    # Extract learner interests.
    raw_interests = learner_profile.get("interest_topics")

    if raw_interests is None:
        raw_interests = learner_profile.get("interests")

    if raw_interests is None:
        raw_interests = []

    if isinstance(raw_interests, str):
        interests = [
            item.strip()
            for item in raw_interests.replace(",", ";").split(";")
            if item.strip()
        ]
    elif isinstance(raw_interests, list):
        interests = [
            item.strip()
            for item in raw_interests
            if isinstance(item, str) and item.strip()
        ]
    else:
        interests = []

    topics_dict: dict[str, Any] = {}

    for item in topic_masteries or []:
        source_topic_id = item.get("source_topic_id")
        raw_topic_id = item.get("topic_id")

        if source_topic_id:
            ai_topic_id = str(source_topic_id)
        elif isinstance(raw_topic_id, str):
            ai_topic_id = raw_topic_id
        elif raw_topic_id is not None and backend_topic_id_map is not None:
            ai_topic_id = backend_topic_id_map.get(int(raw_topic_id))
        else:
            ai_topic_id = None

        if not ai_topic_id:
            raise ValueError(
                "Cannot map backend topic ID to an AI topic ID. "
                "Provide source_topic_id or backend_topic_id_map."
            )

        score = item.get("mastery_score")
        if score is None:
            score = item.get("score")

        topics_dict[ai_topic_id] = {
            "score": float(score) if score is not None else None
        }

    return {
        "learner_id": learner_id,
        "daily_minutes": daily_minutes,
        "topics": topics_dict,
        "course": course,
        "goal": goal,
        "level": level,
        "interests": interests,
    }


def to_frontend_format(
    plan: dict[str, Any],
    course_id: int | None = None,
    topic_id_map: Mapping[str, int] | None = None,
) -> list[dict[str, Any]]:
    """Convert an AI study plan into backend-compatible recommendation cards.

    topic_id_map maps AI source_topic_id -> database Topic.id.
    It must be built from actual backend topic records.
    """

    try:
        user_id = int(plan.get("learner_id", 1))
    except (ValueError, TypeError):
        user_id = 1

    recommendations = []
    recommended_topics = plan.get("recommended_topics", [])

    for idx, item in enumerate(recommended_topics, start=1):
        topic_key = item.get("topic") or item.get("topic_id")

        if not isinstance(topic_key, str) or not topic_key.strip():
            raise ValueError(
                "Every recommended topic must have a valid string topic ID."
            )

        if topic_id_map is None:
            raise ValueError(
                "topic_id_map is required to convert AI topic IDs "
                "into backend database topic IDs."
            )

        if topic_key not in topic_id_map:
            raise ValueError(
                f"No backend database ID found for AI topic '{topic_key}'."
            )

        database_topic_id = topic_id_map[topic_key]
        if (
            isinstance(database_topic_id, bool)
            or not isinstance(database_topic_id, int)
            or database_topic_id <= 0
        ):
            raise ValueError(
                f"Invalid database topic ID for '{topic_key}'."
            )

        activity = item["activity"]
        config = ACTIVITY_CARD_CONFIG.get(
            activity,
            ACTIVITY_CARD_CONFIG["revise"],
        )

        recommendation_card = {
            "id": idx,
            "user_id": user_id,
            "course_id": course_id,
            "topic_id": database_topic_id,
            "recommendation_type": config["type"],
            "title": (
                f"{config['title']}: "
                f"{topic_key.replace('_', ' ').title()}"
            ),
            "description": (
                f"{config['desc_template']} "
                f"(Allocated: {item['minutes']} mins)"
            ),
            "reason": item.get("reason") or plan.get("reason"),
            "priority": config["priority"],
            "status": "pending",
        }

        recommendations.append(recommendation_card)

    return recommendations
