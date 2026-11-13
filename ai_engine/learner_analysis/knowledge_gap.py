
"""
knowledge_gap.py

Identifies a learner's knowledge gaps using topic-wise mastery scores.

Uses mastery_level() from shared schemas.py.
Does not duplicate mastery thresholds.
"""

from ai_engine.common.schemas import mastery_level


def identify_knowledge_gaps(mastery):
    """
    Classify topics according to their mastery scores.

    Args:
        mastery (dict):
            {
                "variables": 90,
                "loops": 33,
                "functions": None
            }

    Returns:
        dict containing weak, developing, good, strong,
        and not-assessed topics.
    """

    if not isinstance(mastery, dict):
        raise ValueError("mastery must be a dictionary")

    result = {
        "weak_topics": [],
        "developing_topics": [],
        "good_topics": [],
        "strong_topics": [],
        "not_assessed": []
    }

    for topic, score in mastery.items():

        if not isinstance(topic, str) or not topic.strip():
            raise ValueError("Topic IDs must be non-empty strings")

        level = mastery_level(score)

        if level == "weak":
            result["weak_topics"].append(topic)

        elif level == "developing":
            result["developing_topics"].append(topic)

        elif level == "good":
            result["good_topics"].append(topic)

        elif level == "strong":
            result["strong_topics"].append(topic)

        elif level == "not_assessed":
            result["not_assessed"].append(topic)

    return result
