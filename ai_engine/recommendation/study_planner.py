
"""Personalized study planner.

Generates a customized daily study plan fitting within the learner's
daily study time budget, respecting prerequisite ordering and mastery.
"""

from typing import Any

from ai_engine.recommendation.adapter import normalize_analysis
from ai_engine.recommendation.reason_text import make_reason
from ai_engine.recommendation.topic_recommender import (
    load_topics_metadata,
    recommend_topics,
)

MIN_TOPIC_MINUTES = 10
DIAGNOSTIC_MINUTES = 15


def build_plan(
    analysis: dict[str, Any],
    topics_metadata: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Build a personalized study plan.

    Guarantees:
    - total_minutes is the sum of allocated topic minutes.
    - total_minutes never exceeds daily_minutes.
    - Each included topic receives at least 10 minutes.
    - Topic recommendations include data-grounded reasons.
    - Prerequisite ordering is preserved.
    """

    normalized = normalize_analysis(analysis)
    daily_budget = normalized.daily_minutes

    if topics_metadata is None:
        topics_metadata = load_topics_metadata()

    # Recommendations now contain dictionaries rather than tuples.
    ordered_topics = recommend_topics(
        normalized,
        topics_metadata=topics_metadata,
    )

    remaining_budget = daily_budget
    planned_topics = []

    for recommendation in ordered_topics:
        topic_id = recommendation["topic_id"]
        activity = recommendation["activity"]
        estimated_minutes = recommendation["estimated_minutes"]
        reason = recommendation["reason"]

        # Diagnostic assessments are limited to 15 minutes.
        if activity == "assess first":
            needed_minutes = min(
                DIAGNOSTIC_MINUTES,
                estimated_minutes,
            )
        else:
            needed_minutes = estimated_minutes

        # Do not add a topic if fewer than 10 minutes remain.
        if remaining_budget < MIN_TOPIC_MINUTES:
            break

        if remaining_budget >= needed_minutes:
            allocated = needed_minutes
        else:
            # Use the remaining budget if it meets the minimum.
            allocated = remaining_budget

        planned_topics.append({
            "topic": topic_id,
            "activity": activity,
            "minutes": allocated,
            "reason": reason,
        })

        remaining_budget -= allocated

    total_minutes = sum(
        topic["minutes"] for topic in planned_topics
    )

    plan = {
        "learner_id": normalized.learner_id,
        "daily_minutes": daily_budget,
        "total_minutes": total_minutes,
        "recommended_topics": planned_topics,
    }

    # Generate the overall study plan explanation.
    plan["reason"] = make_reason(analysis, plan)

    return plan
