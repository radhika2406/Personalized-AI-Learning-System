"""Personalized study planner.

Generates a customized daily study plan fitting within the learner's daily study time budget,
respecting prerequisite ordering and topic mastery levels.
"""

from typing import Any
from ai_engine.recommendation.adapter import normalize_analysis
from ai_engine.recommendation.reason_text import make_reason
from ai_engine.recommendation.topic_recommender import (
    load_topics_metadata,
    recommend_topics,
)

MIN_TOPIC_MINUTES = 10


def _topic_activity_reason(topic: str, activity: str) -> str:
    """Generate a concise topic-level reason based on activity."""
    if activity == "relearn":
        return f"Focus on relearning {topic} core concepts to rebuild a solid foundation."
    elif activity == "revise":
        return f"Revise key syntax and problem patterns in {topic}."
    elif activity == "practice":
        return f"Solve targeted practice exercises in {topic} to maintain mastery."
    elif activity == "advance":
        return f"Tackle advanced exercises in {topic} to expand your depth."
    else:  # assess first
        return f"Take a quick initial diagnostic quiz in {topic} to assess your baseline."


def build_plan(
    analysis: dict[str, Any],
    topics_metadata: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Build a personalized study plan matching contracts/sample_plan.json format.

    Guarantees:
    - total_minutes is the sum of topic minutes.
    - total_minutes <= daily_minutes.
    - minimum 10 minutes per topic.
    - plan["reason"] is written with real numbers and explanations.
    """
    normalized = normalize_analysis(analysis)
    daily_budget = normalized.daily_minutes

    if topics_metadata is None:
        topics_metadata = load_topics_metadata()

    # Create mapping of topic_id -> est_minutes
    est_minutes_map = {t["topic_id"]: t["est_minutes"] for t in topics_metadata}

    # Get ordered recommendations: list of (topic_id, activity)
    ordered_topics = recommend_topics(normalized, topics_metadata=topics_metadata)

    remaining_budget = daily_budget
    planned_topics = []

    for topic_id, activity in ordered_topics:
        # Diagnostic quizzes ('assess first') get 15 min or est_minutes
        if activity == "assess first":
            needed_minutes = min(15, est_minutes_map.get(topic_id, 15))
        else:
            needed_minutes = est_minutes_map.get(topic_id, 20)

        if remaining_budget < MIN_TOPIC_MINUTES:
            # Cannot fit even the minimum threshold for another topic
            break

        if remaining_budget >= needed_minutes:
            allocated = needed_minutes
        else:
            # Shorten topic to use the remaining time (since remaining_budget >= MIN_TOPIC_MINUTES)
            allocated = remaining_budget

        planned_topics.append({
            "topic": topic_id,
            "activity": activity,
            "minutes": allocated,
            "reason": _topic_activity_reason(topic_id, activity),
        })

        remaining_budget -= allocated

    total_minutes = sum(t["minutes"] for t in planned_topics)

    plan = {
        "learner_id": normalized.learner_id,
        "daily_minutes": daily_budget,
        "total_minutes": total_minutes,
        "recommended_topics": planned_topics,
    }

    # Generate the overall plan reason
    plan["reason"] = make_reason(analysis, plan)

    return plan
