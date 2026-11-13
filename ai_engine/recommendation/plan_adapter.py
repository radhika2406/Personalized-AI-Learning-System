"""Adapter layer between AI engine and backend/frontend formats.

Enables seamless two-way transformation without modifying existing backend or frontend code:
- from_backend_format: translates backend database models to learner analysis JSON
- to_frontend_format: translates study-plan JSON to frontend recommendation card objects
"""

from typing import Any

# Activity to recommendation title and priority mapping
ACTIVITY_CARD_CONFIG = {
    "relearn": {
        "title": "Relearn Topic",
        "type": "quiz_performance",
        "priority": 4,
        "desc_template": "Focus on relearning fundamental concepts and retrying practice quizzes.",
    },
    "revise": {
        "title": "Revise Topic",
        "type": "quiz_performance",
        "priority": 3,
        "desc_template": "Review key learning materials and reinforce core programming patterns.",
    },
    "assess first": {
        "title": "Initial Assessment",
        "type": "learning_progress",
        "priority": 3,
        "desc_template": "Complete an initial quiz to assess your knowledge in this topic.",
    },
    "practice": {
        "title": "Strengthen Your Learning",
        "type": "quiz_performance",
        "priority": 2,
        "desc_template": "Solve practical programming problems to keep your skills sharp.",
    },
    "advance": {
        "title": "Advanced Learning",
        "type": "learning_progress",
        "priority": 1,
        "desc_template": "Tackle advanced challenges to expand your mastery.",
    },
}


def from_backend_format(
    learner_profile: dict[str, Any],
    topic_masteries: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Convert backend database models (LearnerProfile & TopicMastery) to our learner analysis format."""
    learner_id = str(learner_profile.get("user_id") or learner_profile.get("id") or "learner_01")
    daily_minutes = int(
        learner_profile.get("daily_study_minutes")
        or learner_profile.get("daily_minutes")
        or 60
    )

    topics_dict: dict[str, Any] = {}

    if topic_masteries:
        for item in topic_masteries:
            tid = str(item.get("topic_id") or item.get("topic") or "")
            score = item.get("mastery_score")
            if score is None:
                score = item.get("score")
            if tid:
                topics_dict[tid] = {
                    "score": float(score) if score is not None else None
                }

    return {
        "learner_id": learner_id,
        "daily_minutes": daily_minutes,
        "topics": topics_dict,
    }


def to_frontend_format(plan: dict[str, Any], course_id: int = 1) -> list[dict[str, Any]]:
    """Convert study plan JSON into recommendation cards expected by frontend/src/pages/Recommendations.jsx."""
    try:
        user_id = int(plan.get("learner_id", 1))
    except (ValueError, TypeError):
        user_id = 1

    recommendations = []
    recommended_topics = plan.get("recommended_topics", [])

    for idx, item in enumerate(recommended_topics, start=1):
        topic = item["topic"]
        activity = item["activity"]
        config = ACTIVITY_CARD_CONFIG.get(activity, ACTIVITY_CARD_CONFIG["revise"])

        recommendation_card = {
            "id": idx,
            "user_id": user_id,
            "course_id": course_id,
            "topic_id": idx,  # sequential mapped ID
            "recommendation_type": config["type"],
            "title": f"{config['title']}: {topic.replace('_', ' ').title()}",
            "description": f"{config['desc_template']} (Allocated: {item['minutes']} mins)",
            "reason": item.get("reason") or plan.get("reason"),
            "priority": config["priority"],
            "status": "pending",
        }
        recommendations.append(recommendation_card)

    return recommendations
