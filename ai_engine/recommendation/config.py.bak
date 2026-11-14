"""Configuration and temporary baseline settings for the recommendation engine.

This file isolates provisional assumptions (topic list, thresholds, activity mappings).
When Person A provides official schemas in ai_engine.common.schemas, this module
can dynamically import them or be replaced without rewriting recommendation logic.
"""

# Default topic list in standard curriculum order
DEFAULT_TOPICS = [
    "variables",
    "data_types",
    "conditions",
    "loops",
    "functions",
    "lists",
]

# Mastery levels
LEVEL_WEAK = "weak"
LEVEL_DEVELOPING = "developing"
LEVEL_GOOD = "good"
LEVEL_STRONG = "strong"
LEVEL_NOT_ASSESSED = "not assessed"

# Activity mapping for each mastery level
ACTIVITY_MAP = {
    LEVEL_WEAK: "relearn",
    LEVEL_DEVELOPING: "revise",
    LEVEL_GOOD: "practice",
    LEVEL_STRONG: "advance",
    LEVEL_NOT_ASSESSED: "assess first",
}


def get_mastery_level(score: float | int | None) -> str:
    """Determine the mastery level for a given percentage score.

    Rules:
    - None (JSON null) means 'not assessed' (never treat as 0).
    - score < 40: weak (e.g., 33% is weak)
    - 40 <= score < 70: developing
    - 70 <= score < 85: good
    - score >= 85: strong
    """
    # If shared schemas module is provided by Person A later, prefer it
    try:
        from ai_engine.common.schemas import mastery_level as official_mastery_level
        return official_mastery_level(score)
    except ImportError:
        pass

    if score is None:
        return LEVEL_NOT_ASSESSED

    if score < 40:
        return LEVEL_WEAK
    elif score < 70:
        return LEVEL_DEVELOPING
    elif score < 85:
        return LEVEL_GOOD
    else:
        return LEVEL_STRONG


def get_activity_for_level(level: str) -> str:
    """Return the designated study activity for a mastery level."""
    return ACTIVITY_MAP.get(level, "assess first")
