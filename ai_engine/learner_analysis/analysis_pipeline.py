
"""
analysis_pipeline.py

Connects performance analysis, mastery calculation,
and knowledge gap identification into one pipeline.
"""

from ai_engine.learner_analysis.performance_analysis import (
    analyze_performance
)
from ai_engine.learner_analysis.mastery import build_mastery
from ai_engine.learner_analysis.knowledge_gap import (
    identify_knowledge_gaps
)


def analyze_learner(quiz_results, course_id, learner_id=None):
    """
    Generate a complete learner analysis.

    Args:
        quiz_results (list): List of quiz result dictionaries.
        course_id (str): Course ID, e.g. 'python' or 'java'.
        learner_id (str, optional): Learner's ID.

    Returns:
        dict: Complete learner analysis.
    """

    if not isinstance(quiz_results, list):
        raise ValueError("quiz_results must be a list")

    if not isinstance(course_id, str) or not course_id.strip():
        raise ValueError("A valid course_id is required")

    if not quiz_results:
        raise ValueError("At least one quiz result is required")

    # Step 1: Performance analysis
    performance = analyze_performance(quiz_results)

    # Step 2: Calculate topic-wise mastery
    mastery = build_mastery(
        quiz_results,
        course_id=course_id
    )

    # Step 3: Identify knowledge gaps
    knowledge_gaps = identify_knowledge_gaps(mastery)

    # Step 4: Identify learner ID if not provided
    if learner_id is None:
        learner_id = quiz_results[0].get("learner_id")

    # Step 5: Combine all results
    return {
        "learner_id": learner_id,
        "course": course_id,
        "mastery": mastery,
        **knowledge_gaps,
        "performance": performance
    }
