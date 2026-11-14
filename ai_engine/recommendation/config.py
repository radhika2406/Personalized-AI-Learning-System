"""Configuration and baseline settings for the recommendation engine.

Directly imports definitions from Person A's ai_engine.common.schemas (the source of truth).
"""

from ai_engine.common.schemas import (
    TOPICS as DEFAULT_TOPICS,
    MASTERY_LEVELS,
    NOT_ASSESSED,
    mastery_level,
)


"""Configuration and baseline settings for the recommendation engine."""

# Prefer the official shared topic list.
try:
    from ai_engine.common.schemas import TOPICS

    DEFAULT_TOPICS = list(TOPICS)

except ImportError:
    # Fallback only when shared schemas are unavailable.
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
LEVEL_NOT_ASSESSED = NOT_ASSESSED
LEVEL_NOT_ASSESSED = "not_assessed"


# Activity mapping for each mastery level
ACTIVITY_MAP = {
    LEVEL_WEAK: "relearn",
    LEVEL_DEVELOPING: "revise",
    LEVEL_GOOD: "practice",
    LEVEL_STRONG: "advance",
    LEVEL_NOT_ASSESSED: "assess first",
    "not assessed": "assess first",  # alias if string with space is passed
}


def get_mastery_level(score: float | int | None) -> str:
    """Use the official shared mastery thresholds."""

    try:
        from ai_engine.common.schemas import mastery_level

        return mastery_level(score)

    except ImportError:
        # Temporary fallback if shared schemas are unavailable.
        if score is None:
            return LEVEL_NOT_ASSESSED

        if score < 40:
            return LEVEL_WEAK
        elif score < 60:
            return LEVEL_DEVELOPING
        elif score < 80:
            return LEVEL_GOOD
        else:
            return LEVEL_STRONG
    """Determine the mastery level for a given percentage score using schemas.mastery_level()."""
    return mastery_level(score)


def get_activity_for_level(level: str) -> str:
    """Return the designated activity for a mastery level."""

    return ACTIVITY_MAP.get(level, "assess first")
