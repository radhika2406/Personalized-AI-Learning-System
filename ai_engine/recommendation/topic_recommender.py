"""Topic recommender engine.

Recommends study topics ordered by greatest learning need while strictly
respecting prerequisite requirements.
"""

import csv
from pathlib import Path
from typing import Any

from ai_engine.recommendation.adapter import normalize_analysis, NormalizedLearner
from ai_engine.recommendation.config import (
    DEFAULT_TOPICS,
    LEVEL_WEAK,
    LEVEL_DEVELOPING,
    LEVEL_NOT_ASSESSED,
    LEVEL_GOOD,
    LEVEL_STRONG,
    get_mastery_level,
    get_activity_for_level,
)


def load_topics_metadata(csv_path: str | Path | None = None) -> list[dict[str, Any]]:
    """Load topic metadata from topics.csv.

    Returns a list of dicts with:
    - topic_id (str)
    - course (str)
    - order (int)
    - prerequisites (list of str)
    - est_minutes (int)
    """
    if csv_path is None:
        # Default location: assessment/content/topics.csv relative to this file
        current_dir = Path(__file__).resolve().parent
        csv_path = current_dir.parent.parent / "assessment" / "content" / "topics.csv"

    path = Path(csv_path)
    if not path.is_file():
        # Fallback to default topics if CSV is not found
        return [
            {
                "topic_id": topic,
                "course": "python",
                "order": idx + 1,
                "prerequisites": [],
                "est_minutes": 20,
            }
            for idx, topic in enumerate(DEFAULT_TOPICS)
        ]

    topics = []
    with open(path, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            prereqs_raw = row.get("prerequisites", "").strip()
            prereqs = [p.strip() for p in prereqs_raw.split(";") if p.strip()] if prereqs_raw else []

            topics.append({
                "topic_id": row["topic_id"].strip(),
                "course": row.get("course", "python").strip(),
                "order": int(row.get("order", 0)),
                "prerequisites": prereqs,
                "est_minutes": int(row.get("est_minutes", 20)),
            })

    # Sort topics by defined curriculum order
    topics.sort(key=lambda t: t["order"])
    return topics


def _urgency_key(topic_id: str, level: str, score: float | None, order: int) -> tuple[int, float, int]:
    """Calculate sorting key for learning urgency (lower key = higher priority).

    Urgency ranks:
    0: weak (lowest score first)
    1: developing (lowest score first)
    2: not assessed (ordered by curriculum sequence)
    3: good (lowest score first)
    4: strong (lowest score first)
    """
    if level == LEVEL_WEAK:
        return (0, score if score is not None else 0.0, order)
    elif level == LEVEL_DEVELOPING:
        return (1, score if score is not None else 50.0, order)
    elif level == LEVEL_NOT_ASSESSED:
        return (2, 0.0, order)
    elif level == LEVEL_GOOD:
        return (3, score if score is not None else 75.0, order)
    else:  # LEVEL_STRONG
        return (4, score if score is not None else 90.0, order)


def recommend_topics(
    analysis: dict[str, Any] | NormalizedLearner,
    topics_metadata: list[dict[str, Any]] | None = None,
) -> list[tuple[str, str]]:
    """Recommend topics in order of priority, respecting prerequisite rules.

    Parameters:
    - analysis: Raw learner analysis dict or NormalizedLearner instance.
    - topics_metadata: Optional list of topic metadata dictionaries.

    Returns:
    - Ordered list of (topic_id, activity) tuples.
    """
    # Step 1: Normalize learner analysis
    if isinstance(analysis, NormalizedLearner):
        normalized = analysis
    else:
        normalized = normalize_analysis(analysis)

    # Step 2: Load topic metadata
    if topics_metadata is None:
        topics_metadata = load_topics_metadata()

    # Build lookup map for topic metadata
    metadata_map = {t["topic_id"]: t for t in topics_metadata}

    # Include any topics present in metadata
    all_topic_ids = [t["topic_id"] for t in topics_metadata]

    # Step 3: Determine mastery level and activity for each topic
    topic_info = {}
    for tid in all_topic_ids:
        score = normalized.topic_scores.get(tid)
        level = get_mastery_level(score)
        activity = get_activity_for_level(level)
        order = metadata_map[tid]["order"]

        # Prerequisite is considered 'satisfied' if learner is at 'good' or 'strong'
        prereqs = metadata_map[tid]["prerequisites"]
        satisfied = level in (LEVEL_GOOD, LEVEL_STRONG)

        topic_info[tid] = {
            "topic_id": tid,
            "score": score,
            "level": level,
            "activity": activity,
            "order": order,
            "prerequisites": prereqs,
            "is_mastered": satisfied,
        }

    # Step 4: Iteratively select the next best topic to recommend
    # A topic can only be scheduled if all its prerequisites that are NOT YET
    # at 'good' or above have already been scheduled.
    scheduled: list[str] = []
    remaining = set(all_topic_ids)

    while remaining:
        # Find candidates whose unsaved/unmastered prerequisites are all scheduled
        eligible = []
        for tid in remaining:
            info = topic_info[tid]
            unmastered_prereqs = [
                p for p in info["prerequisites"]
                if p in topic_info and not topic_info[p]["is_mastered"]
            ]

            # All unmastered prerequisites must have already been scheduled
            if all(p in scheduled for p in unmastered_prereqs):
                eligible.append(tid)

        if not eligible:
            # Fallback for unexpected circular dependencies: pick lowest order remaining
            eligible = sorted(list(remaining), key=lambda x: topic_info[x]["order"])

        # Pick the most urgent topic among eligible
        best_topic = min(
            eligible,
            key=lambda tid: _urgency_key(
                tid,
                topic_info[tid]["level"],
                topic_info[tid]["score"],
                topic_info[tid]["order"],
            ),
        )

        scheduled.append(best_topic)
        remaining.remove(best_topic)

    # Step 5: Format output as (topic_id, activity) tuples
    return [(tid, topic_info[tid]["activity"]) for tid in scheduled]
