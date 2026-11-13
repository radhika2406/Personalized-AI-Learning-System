"""Adapter layer to normalize learner analysis input.

This module converts various input shapes (provisional JSON, backend database fields,
or future contracts from Person A) into a consistent internal format.
"""

from dataclasses import dataclass
from typing import Any


@dataclass
class NormalizedLearner:
    """Internal standardized representation of learner analysis."""
    learner_id: str
    daily_minutes: int
    topic_scores: dict[str, float | None]


def normalize_analysis(data: dict[str, Any]) -> NormalizedLearner:
    """Normalize a learner analysis dictionary into a standard NormalizedLearner.

    Supports:
    - daily_minutes or daily_study_minutes
    - topics as a dictionary of objects, dictionary of numbers, or list of objects
    """
    learner_id = str(data.get("learner_id") or data.get("user_id") or "anonymous_learner")

    daily_minutes = int(
        data.get("daily_minutes")
        or data.get("daily_study_minutes")
        or 60
    )

    raw_topics = data.get("topics") or data.get("topic_mastery") or {}
    topic_scores: dict[str, float | None] = {}

    if isinstance(raw_topics, dict):
        for topic_id, val in raw_topics.items():
            if val is None:
                topic_scores[topic_id] = None
            elif isinstance(val, (int, float)):
                topic_scores[topic_id] = float(val)
            elif isinstance(val, dict):
                score_val = val.get("score")
                if score_val is None:
                    score_val = val.get("mastery_score")
                topic_scores[topic_id] = float(score_val) if score_val is not None else None
            else:
                topic_scores[topic_id] = None

    elif isinstance(raw_topics, list):
        for item in raw_topics:
            if isinstance(item, dict):
                topic_id = str(item.get("topic_id") or item.get("topic") or "")
                if topic_id:
                    score_val = item.get("score")
                    if score_val is None:
                        score_val = item.get("mastery_score")
                    topic_scores[topic_id] = float(score_val) if score_val is not None else None

    return NormalizedLearner(
        learner_id=learner_id,
        daily_minutes=daily_minutes,
        topic_scores=topic_scores,
    )
