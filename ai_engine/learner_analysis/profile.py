
"""
profile.py

Validates a learner profile before it is used by other modules.
Supports all registered courses.
Returns a list of error messages. An empty list means valid.
"""

from ai_engine.common.course_config import get_course
from ai_engine.common.schemas import (
    LEVELS,
    MIN_DAILY_MINUTES,
    MAX_DAILY_MINUTES,
)


def validate_profile(profile):
    """Return a list of validation errors. [] means valid."""

    if not isinstance(profile, dict):
        return ["profile must be a dictionary"]

    errors = []

    # Learner ID
    learner_id = profile.get("learner_id")
    if not isinstance(learner_id, str) or not learner_id.strip():
        errors.append("learner_id is missing")

    # Course: accept any registered course
    course = profile.get("course")
    if not isinstance(course, str) or not get_course(course):
        errors.append("course must be a registered course")

    # Learning goal
    goal = profile.get("goal")
    if not isinstance(goal, str) or not goal.strip():
        errors.append("goal is missing")

    # Self-reported learner level
    if profile.get("level") not in LEVELS:
        errors.append("level must be beginner, intermediate or advanced")

    # Daily study time
    minutes = profile.get("daily_minutes")

    if (
        isinstance(minutes, bool)
        or not isinstance(minutes, int)
        or minutes < MIN_DAILY_MINUTES
        or minutes > MAX_DAILY_MINUTES
    ):
        errors.append(
            f"daily_minutes must be a whole number from "
            f"{MIN_DAILY_MINUTES} to {MAX_DAILY_MINUTES}"
        )

    return errors
