
"""
diagnostic_report.py

Generates a structured learner diagnostic report
from initial assessment results.
"""

from ai_engine.common.course_config import get_course
from ai_engine.common.schemas import mastery_level
from assessment.question_management.loader import load_course_topics


def generate_diagnostic_report(assessment_result):
    """
    Generate a diagnostic report from initial assessment results.

    Identifies:
    - Overall learner level
    - Strong topics
    - Good topics
    - Developing topics
    - Weak topics
    - Recommended starting topics
    """

    if not isinstance(assessment_result, dict):
        raise ValueError("assessment_result must be a dictionary")

    learner_id = assessment_result.get("learner_id")
    course_id = assessment_result.get("course_id")

    if not isinstance(learner_id, str) or not learner_id.strip():
        raise ValueError("Invalid learner_id")

    if not isinstance(course_id, str) or not get_course(course_id):
        raise ValueError("Invalid course_id")

    score = assessment_result.get("overall_score_pct")

    if (
        isinstance(score, bool)
        or not isinstance(score, (int, float))
        or not 0 <= score <= 100
    ):
        raise ValueError("Invalid overall assessment score")

    topic_results = assessment_result.get("topic_results")

    if not isinstance(topic_results, dict) or not topic_results:
        raise ValueError("topic_results must be a non-empty dictionary")

    topics = load_course_topics(course_id)

    valid_topics = {
        topic.get("id") or topic.get("topic_id"): topic
        for topic in topics
    }

    categories = {
        "weak_topics": [],
        "developing_topics": [],
        "good_topics": [],
        "strong_topics": [],
    }

    for topic_id, result in topic_results.items():

        if topic_id not in valid_topics:
            raise ValueError(f"Unknown topic: {topic_id}")

        if not isinstance(result, dict):
            raise ValueError(
                f"Invalid result for topic '{topic_id}'"
            )

        topic_score = result.get("score_pct")

        if (
            isinstance(topic_score, bool)
            or not isinstance(topic_score, (int, float))
            or not 0 <= topic_score <= 100
        ):
            raise ValueError(
                f"Invalid score for topic '{topic_id}'"
            )

        level = mastery_level(topic_score)

        if level == "weak":
            categories["weak_topics"].append(topic_id)

        elif level == "developing":
            categories["developing_topics"].append(topic_id)

        elif level == "good":
            categories["good_topics"].append(topic_id)

        elif level == "strong":
            categories["strong_topics"].append(topic_id)

    # Recommended starting topics are weak topics first,
    # followed by developing topics.
    recommended_starting_topics = (
        categories["weak_topics"]
        + categories["developing_topics"]
    )

    # If no weak or developing topics exist, start with
    # the next unassessed topic or the first course topic.
    if not recommended_starting_topics:
        recommended_starting_topics = [
            topic.get("id") or topic.get("topic_id")
            for topic in topics
            if (
                topic.get("id") or topic.get("topic_id")
            ) not in topic_results
        ]

    return {
        "learner_id": learner_id,
        "course_id": course_id,
        "overall_score_pct": score,
        "initial_level": assessment_result.get("initial_level"),
        "total_topics": len(topics),
        "assessed_topics": len(topic_results),
        "strong_topics": categories["strong_topics"],
        "good_topics": categories["good_topics"],
        "developing_topics": categories["developing_topics"],
        "weak_topics": categories["weak_topics"],
        "recommended_starting_topics": recommended_starting_topics,
    }
