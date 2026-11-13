"""Adaptive learning engine.

Dynamically adapts the personalized study plan when a new quiz result or learner
analysis is received, tracking what changed in the plan.
"""

from typing import Any
from ai_engine.recommendation.study_planner import build_plan
from ai_engine.recommendation.topic_recommender import recommend_topics
from ai_engine.recommendation.adapter import normalize_analysis
from ai_engine.recommendation.config import get_mastery_level, LEVEL_GOOD, LEVEL_STRONG


def adapt_plan(
    previous_analysis: dict[str, Any],
    new_analysis: dict[str, Any],
) -> dict[str, Any]:
    """Adapt study plan based on updated learner analysis and summarize changes.

    Parameters:
    - previous_analysis: The earlier learner analysis state.
    - new_analysis: The newly generated learner analysis (from Person A after a quiz).

    Returns:
    - dict containing:
      - 'plan': The newly generated study plan.
      - 'changes': List of human-readable descriptions of what changed.
    """
    old_norm = normalize_analysis(previous_analysis)
    new_norm = normalize_analysis(new_analysis)

    old_plan = build_plan(previous_analysis)
    new_plan = build_plan(new_analysis)

    old_recs = recommend_topics(previous_analysis)
    new_recs = recommend_topics(new_analysis)

    old_activities = dict(old_recs)
    new_activities = dict(new_recs)

    old_topics_order = [t["topic"] for t in old_plan.get("recommended_topics", [])]
    new_topics_order = [t["topic"] for t in new_plan.get("recommended_topics", [])]

    changes = []

    # 1. Detect activity changes
    all_topics = set(old_activities.keys()) | set(new_activities.keys())
    for topic in sorted(all_topics):
        old_act = old_activities.get(topic)
        new_act = new_activities.get(topic)

        if old_act and new_act and old_act != new_act:
            changes.append(f"Topic '{topic}' activity changed from '{old_act}' to '{new_act}'.")
        elif not old_act and new_act:
            changes.append(f"Topic '{topic}' was added to the plan with activity '{new_act}'.")
        elif old_act and not new_act:
            changes.append(f"Topic '{topic}' was completed or removed from the active daily plan.")

    # 2. Detect position / priority shifts
    common_topics = [t for t in new_topics_order if t in old_topics_order]
    for topic in common_topics:
        old_pos = old_topics_order.index(topic) + 1
        new_pos = new_topics_order.index(topic) + 1
        if new_pos < old_pos:
            changes.append(f"Topic '{topic}' moved up in priority from position {old_pos} to {new_pos}.")
        elif new_pos > old_pos:
            changes.append(f"Topic '{topic}' moved down in priority from position {old_pos} to {new_pos}.")

    # 3. Detect prerequisite unlocking
    for topic, new_score in new_norm.topic_scores.items():
        old_score = old_norm.topic_scores.get(topic)
        old_lvl = get_mastery_level(old_score)
        new_lvl = get_mastery_level(new_score)

        if old_lvl not in (LEVEL_GOOD, LEVEL_STRONG) and new_lvl in (LEVEL_GOOD, LEVEL_STRONG):
            changes.append(
                f"Prerequisite '{topic}' achieved '{new_lvl}' mastery, unlocking dependent advanced topics."
            )

    if not changes:
        changes.append("No significant changes in topic priorities or activities.")

    return {
        "plan": new_plan,
        "changes": changes,
    }
