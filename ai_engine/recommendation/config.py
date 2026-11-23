
"""Configuration and baseline settings for the recommendation engine."""

from ai_engine.common.schemas import (
    TOPICS,
    NOT_ASSESSED,
    mastery_level,
)

# Official shared topic list
DEFAULT_TOPICS = list(TOPICS)

# Mastery levels
LEVEL_WEAK = "weak"
LEVEL_DEVELOPING = "developing"
LEVEL_GOOD = "good"
LEVEL_STRONG = "strong"
LEVEL_NOT_ASSESSED = NOT_ASSESSED

# Activity mapping
ACTIVITY_MAP = {
    LEVEL_WEAK: "relearn",
    LEVEL_DEVELOPING: "revise",
    LEVEL_GOOD: "practice",
    LEVEL_STRONG: "advance",
    LEVEL_NOT_ASSESSED: "assess first",
    "not assessed": "assess first",
}


def get_mastery_level(score: float | int | None) -> str:
    """Use the official shared mastery thresholds."""
    return mastery_level(score)


def get_activity_for_level(level: str) -> str:
    """Return the designated activity for a mastery level."""
    return ACTIVITY_MAP.get(level, "assess first")
