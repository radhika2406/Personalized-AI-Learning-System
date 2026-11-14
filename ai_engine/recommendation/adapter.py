"""Adapter layer to normalize learner analysis input.

This module converts various input shapes (sample_analysis.json, backend database fields,
or custom test dictionaries) into a consistent internal format.
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
    - mastery dictionary from contracts/sample_analysis.json
    - topics or topic_mastery dictionary or list
    - daily_minutes or daily_study_minutes
    """
    learner_id = str(data.get("learner_id") or data.get("user_id") or "anonymous_learner")

    daily_minutes_val = data.get("daily_minutes") or data.get("daily_study_minutes")
    try:
        daily_minutes = int(daily_minutes_val)
        if daily_minutes <= 0:
            daily_minutes = 60
    except (TypeError, ValueError):
        daily_minutes = 60

    # Look for 'mastery' (official sample_analysis.json key) first, then 'topics' or 'topic_mastery'
    raw_topics = data.get("mastery")
    if raw_topics is None:
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
