
"""Dynamically adapts the personalized study plan when new learner
performance data is received and tracks changes.
"""

from typing import Any

from ai_engine.recommendation.adapter import normalize_analysis
from ai_engine.recommendation.study_planner import build_plan


def _get_recommendations(plan: dict[str, Any]) -> list[dict[str, Any]]:
    """Safely extract recommended topics from a study plan."""
    recommendations = plan.get("recommended_topics", [])

    if not isinstance(recommendations, list):
        return []

    return recommendations


def _get_topic_id(item: dict[str, Any]) -> str | None:
    """Support the topic keys used by recommendation outputs."""
    return item.get("topic_id") or item.get("topic")


def _get_activity(item: dict[str, Any]) -> str | None:
    """Extract the recommended activity."""
    return item.get("activity")


def _get_score(learner: Any, topic_id: str) -> float | None:
    """Get a learner's mastery score for a topic."""
    return learner.topic_scores.get(topic_id)


def _activity_map(plan: dict[str, Any]) -> dict[str, str | None]:
    """Create a topic-to-activity mapping from a study plan."""
    result = {}

    for item in _get_recommendations(plan):
        if not isinstance(item, dict):
            continue

        topic_id = _get_topic_id(item)

        if topic_id:
            result[topic_id] = _get_activity(item)

    return result


def adapt_plan(
    previous_analysis: dict[str, Any],
    new_analysis: dict[str, Any],
) -> dict[str, Any]:
    """
    Compare the previous and updated learner data.

    Returns:
        {
            "plan": updated study plan,
            "changes": list of detected changes
        }
    """

    if not isinstance(previous_analysis, dict):
        raise TypeError("previous_analysis must be a dictionary.")

    if not isinstance(new_analysis, dict):
        raise TypeError("new_analysis must be a dictionary.")

    previous_learner = normalize_analysis(previous_analysis)
    updated_learner = normalize_analysis(new_analysis)

    # Generate the previous and updated study plans.
    previous_plan = build_plan(previous_analysis)
    updated_plan = build_plan(new_analysis)

    previous_activities = _activity_map(previous_plan)
    updated_activities = _activity_map(updated_plan)

    changes: list[str] = []

    # Detect activity changes.
    all_topics = set(previous_activities) | set(updated_activities)

    for topic_id in sorted(all_topics):
        old_activity = previous_activities.get(topic_id)
        new_activity = updated_activities.get(topic_id)

        if old_activity != new_activity:
            if old_activity is None:
                changes.append(
                    f"Topic '{topic_id}' added with activity '{new_activity}'."
                )
            elif new_activity is None:
                changes.append(
                    f"Topic '{topic_id}' removed from recommendations."
                )
            else:
                changes.append(
                    f"Topic '{topic_id}' activity changed "
                    f"from '{old_activity}' to '{new_activity}'."
                )

    # Detect mastery improvements.
    all_scored_topics = (
        set(previous_learner.topic_scores)
        | set(updated_learner.topic_scores)
    )

    for topic_id in sorted(all_scored_topics):
        old_score = _get_score(previous_learner, topic_id)
        new_score = _get_score(updated_learner, topic_id)

        if old_score is None and new_score is not None:
            changes.append(
                f"Topic '{topic_id}' received its first assessment "
                f"score of {new_score:g}."
            )
            continue

        if old_score is None or new_score is None:
            continue

        if new_score > old_score:
            changes.append(
                f"Topic '{topic_id}' mastery improved "
                f"from {old_score:g} to {new_score:g}."
            )
        elif new_score < old_score:
            changes.append(
                f"Topic '{topic_id}' mastery decreased "
                f"from {old_score:g} to {new_score:g}."
            )

    # Detect prerequisite improvements that may unlock dependent topics.
    for topic_id in sorted(all_scored_topics):
        old_score = _get_score(previous_learner, topic_id)
        new_score = _get_score(updated_learner, topic_id)

        if old_score is None and new_score is not None:
            if new_score >= 60:
                changes.append(
                    f"Prerequisite '{topic_id}' achieved a good mastery level."
                )
        elif (
            old_score is not None
            and new_score is not None
            and old_score < 60
            and new_score >= 60
        ):
            changes.append(
                f"Prerequisite '{topic_id}' achieved a good mastery level."
            )

    return {
        "plan": updated_plan,
        "changes": changes,
    }
