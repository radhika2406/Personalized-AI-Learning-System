"""
schemas.py  (shared by Person A and Person B)

This file holds the things we AGREED on, written as code, so nobody
types the same name differently in two places.
Change something here only after both of you agree, then tell Members 1 and 2.
"""

# ----- Course and topics -----
COURSE = "python"

# Topic ids: lowercase, underscores. Keep the same order as topics.csv.
TOPICS = ["variables", "conditions", "loops", "functions", "lists", "dictionaries"]

# ----- Learner levels (self-reported, NOT the same as mastery) -----
LEVELS = ["beginner", "intermediate", "advanced"]

# ----- Mastery levels -----
# Each pair is (upper limit, level name). A score below the limit gets that name.
# These are starting values to test and tune, agreed with Member 4.
MASTERY_LEVELS = [
    (40, "weak"),        # 0-39
    (60, "developing"),  # 40-59
    (80, "good"),        # 60-79
    (101, "strong"),     # 80-100
]

NOT_ASSESSED = "not_assessed"  # used when a topic has score None (never quizzed)

# ----- Limits for daily study time (minutes) -----
MIN_DAILY_MINUTES = 10
MAX_DAILY_MINUTES = 480

# ----- Answer letters allowed in a quiz -----
ANSWER_CHOICES = ["a", "b", "c", "d"]


def mastery_level(score):
    """Turn a topic score (0-100) into a level name.

    None means the learner was never quizzed on this topic, so the result is
    'not_assessed'. It must NOT be treated as 0.
    """
    if score is None:
        return NOT_ASSESSED
    if isinstance(score, bool) or not isinstance(score, (int, float)):
        raise ValueError("score must be a number or None")
    if score < 0 or score > 100:
        raise ValueError("score must be between 0 and 100")
    for limit, name in MASTERY_LEVELS:
        if score < limit:
            return name
