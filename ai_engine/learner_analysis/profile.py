"""
profile.py

Checks a new learner profile BEFORE anything else uses it.
Returns a list of error messages. An empty list means the profile is valid.
"""

from ai_engine.common.schemas import (
    COURSE,
    LEVELS,
    MIN_DAILY_MINUTES,
    MAX_DAILY_MINUTES,
)


def validate_profile(profile):
    """Return a list of error strings. [] means the profile is valid."""
    if not isinstance(profile, dict):
        return ["profile must be a dictionary"]

    errors = []

    learner_id = profile.get("learner_id")
    if not isinstance(learner_id, str) or not learner_id.strip():
        errors.append("learner_id is missing")

    if profile.get("course") != COURSE:
        errors.append(f"course must be '{COURSE}'")

    goal = profile.get("goal")
    if not isinstance(goal, str) or not goal.strip():
        errors.append("goal is missing")

    if profile.get("level") not in LEVELS:
        errors.append("level must be beginner, intermediate or advanced")

    minutes = profile.get("daily_minutes")
    # bool is a subtype of int in Python, so True would sneak through without this check
    if (
        isinstance(minutes, bool)
        or not isinstance(minutes, int)
        or minutes < MIN_DAILY_MINUTES
        or minutes > MAX_DAILY_MINUTES
    ):
        errors.append(
            f"daily_minutes must be a whole number from {MIN_DAILY_MINUTES} to {MAX_DAILY_MINUTES}"
        )

    return errors
