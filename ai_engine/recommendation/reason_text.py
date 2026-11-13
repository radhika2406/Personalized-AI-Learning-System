"""Reason text generator for study plans.

Generates 1 to 3 beginner-friendly sentences explaining why the study plan was built,
using real topic names, mastery percentages, and daily minutes.
"""

from typing import Any
from ai_engine.recommendation.adapter import normalize_analysis
from ai_engine.recommendation.config import (
    LEVEL_WEAK,
    LEVEL_DEVELOPING,
    LEVEL_GOOD,
    LEVEL_STRONG,
    LEVEL_NOT_ASSESSED,
    get_mastery_level,
)


def make_reason(analysis: dict[str, Any], plan: dict[str, Any]) -> str:
    """Generate an explanation of the study plan.

    Uses real numbers (topic names, percentages, daily minutes) and provides
    prerequisite explanations when a prerequisite is scheduled first.
    """
    normalized = normalize_analysis(analysis)
    recommended = plan.get("recommended_topics", [])
    daily_minutes = plan.get("daily_minutes", normalized.daily_minutes)

    if not recommended:
        return (
            f"Your daily study budget of {daily_minutes} minutes is below the "
            "minimum required time (10 minutes) for a study topic. "
            "Please allocate at least 10 minutes to generate study recommendations."
        )

    first_item = recommended[0]
    first_topic = first_item["topic"]
    first_activity = first_item["activity"]
    first_minutes = first_item["minutes"]

    first_score = normalized.topic_scores.get(first_topic)
    first_level = get_mastery_level(first_score)

    # Check Case 1: Prerequisite chosen first
    # If the first topic is not assessed or developing, but a subsequent topic is weak (e.g. loops is weak)
    weaker_downstream = None
    for item in recommended[1:]:
        t_score = normalized.topic_scores.get(item["topic"])
        t_level = get_mastery_level(t_score)
        if t_level == LEVEL_WEAK and first_level != LEVEL_WEAK:
            weaker_downstream = item["topic"]
            break

    if weaker_downstream:
        return (
            f"We scheduled {first_topic} first as an essential prerequisite before tackling {weaker_downstream}. "
            f"With your {daily_minutes}-minute daily study budget, completing this foundation will ensure smooth progression."
        )

    # Check Case 2: Everything strong
    all_scores = [s for s in normalized.topic_scores.values() if s is not None]
    if all_scores and all(get_mastery_level(s) == LEVEL_STRONG for s in all_scores):
        score_str = f"{int(round(first_score))}%" if first_score is not None else ""
        return (
            f"You have demonstrated strong mastery across all assessed Python topics! "
            f"Your {daily_minutes}-minute plan focuses on advancing with challenging exercises in {first_topic} ({score_str})."
        )

    # Check Case 3: Not Assessed (Crucial rule: Never say 0%)
    if first_level == LEVEL_NOT_ASSESSED or first_score is None:
        return (
            f"We started your plan with an initial assessment in {first_topic} because it has not been assessed yet. "
            f"This {first_minutes}-minute diagnostic quiz will evaluate your understanding and guide your next learning steps."
        )

    score_pct = f"{int(round(first_score))}%"

    # Check Case 4: Weak
    if first_level == LEVEL_WEAK:
        return (
            f"Your study plan prioritizes {first_topic} ({score_pct} mastery) with {first_minutes} minutes of focused relearning. "
            "Rebuilding this core concept will significantly improve your programming confidence."
        )

    # Check Case 5: Developing
    if first_level == LEVEL_DEVELOPING:
        return (
            f"Your plan dedicates {first_minutes} minutes to revising {first_topic} (currently at {score_pct} mastery). "
            "Focused revision will reinforce key examples and move you toward full mastery."
        )

    # Check Case 6: Good
    if first_level == LEVEL_GOOD:
        return (
            f"You have a good grasp of {first_topic} ({score_pct}). "
            f"Your plan allocates {first_minutes} minutes of targeted practice to refine your problem-solving."
        )

    # Check Case 7: Strong (Single or default strong)
    template_reason = (
        f"You have strong mastery in {first_topic} ({score_pct}). "
        f"We scheduled {first_minutes} minutes to advance into deeper programming concepts."
    )

    # Optional LLM wording enhancement if call_llm is available and successful
    try:
        from ai_engine.llm.ai_explainer import call_llm
        prompt = (
            f"Rewrite this study plan recommendation message for a beginner Python learner in 1 or 2 encouraging sentences: "
            f"'{template_reason}'. Keep the topic name '{first_topic}' and '{score_pct}' exact."
        )
        llm_response = call_llm(prompt)
        if llm_response and len(llm_response.strip()) > 0:
            return llm_response.strip()
    except Exception:
        pass

    return template_reason
