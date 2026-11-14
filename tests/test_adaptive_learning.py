
"""Adaptive learning engine.

Dynamically adapts the personalized study plan when new learner
performance data is received and tracks changes.
"""

from typing import Any

from ai_engine.recommendation.study_planner import build_plan
from ai_engine.recommendation.topic_recommender import recommend_topics
from ai_engine.recommendation.adapter import normalize_analysis
from ai_engine.recommendation.config import (
    get_mastery_level,
    LEVEL_GOOD,
    LEVEL_STRONG,
)


def adapt_plan(
    previous_analysis: dict[str, Any],
    new_analysis: dict[str, Any],
) -> dict[str, Any]:
    """Adapt the study plan and summarize recommendation changes."""

    old_norm = normalize_analysis(previous_analysis)
    new_norm = normalize_analysis(new_analysis)

    old_plan = build_plan(previous_analysis)
    new_plan = build_plan(new_analysis)

    old_recs = recommend_topics(previous_analysis)
    new_recs = recommend_topics(new_analysis)

    # Recommendations now contain dictionaries, not tuples.
    old_activities = {
        item["topic_id"]: item["activity"]
        for item in old_recs
    }

    new_activities = {
        item["topic_id"]: item["activity"]
        for item in new_recs
    }

    old_topics_order = [
        item["topic"]
        for item in old_plan.get("recommended_topics", [])
    ]

    new_topics_order = [
        item["topic"]
        for item in new_plan.get("recommended_topics", [])
    ]

    changes = []

    # 1. Detect activity changes and topic additions/removals.
    all_topics = set(old_activities) | set(new_activities)

    for topic in sorted(all_topics):
        old_activity = old_activities.get(topic)
        new_activity = new_activities.get(topic)

        if old_activity and new_activity and old_activity != new_activity:
            changes.append(
                f"Topic '{topic}' activity changed from "
                f"'{old_activity}' to '{new_activity}'."
            )

        elif not old_activity and new_activity:
            changes.append(
                f"Topic '{topic}' was added to the plan "
                f"with activity '{new_activity}'."
            )

        elif old_activity and not new_activity:
            changes.append(
                f"Topic '{topic}' was completed or removed "
                "from the active daily plan."
            )

    # 2. Detect topic priority changes.
    common_topics = [
        topic for topic in new_topics_order
        if topic in old_topics_order
    ]

    for topic in common_topics:
        old_position = old_topics_order.index(topic) + 1
        new_position = new_topics_order.index(topic) + 1

        if new_position < old_position:
            changes.append(
                f"Topic '{topic}' moved up in priority "
                f"from position {old_position} to {new_position}."
            )

        elif new_position > old_position:
            changes.append(
                f"Topic '{topic}' moved down in priority "
                f"from position {old_position} to {new_position}."
            )

    # 3. Detect mastery improvement to good or strong.
    for topic, new_score in new_norm.topic_scores.items():
        old_score = old_norm.topic_scores.get(topic)

        old_level = get_mastery_level(old_score)
        new_level = get_mastery_level(new_score)

        if (
            old_level not in (LEVEL_GOOD, LEVEL_STRONG)
            and new_level in (LEVEL_GOOD, LEVEL_STRONG)
        ):
            changes.append(
                f"Prerequisite '{topic}' achieved '{new_level}' "
                "mastery, unlocking dependent advanced topics."
            )

    if not changes:
        changes.append(
            "No significant changes in topic priorities or activities."
        )

    return {
        "plan": new_plan,
        "changes": changes,
    }
