
"""
analysis_pipeline.py

Connects performance analysis, mastery calculation,
and knowledge gap identification into one pipeline.
"""

from ai_engine.learner_analysis.performance_analysis import analyze_performance
from ai_engine.learner_analysis.mastery import build_mastery
from ai_engine.learner_analysis.knowledge_gap import identify_knowledge_gaps


def analyze_learner(quiz_results, course_id, learner_id=None):
    """
    Generate a complete learner analysis.

    Empty quiz results are allowed for new learners.
    All identified learner IDs must match.
    """

    if not isinstance(quiz_results, list):
        raise ValueError("quiz_results must be a list")

    if not isinstance(course_id, str) or not course_id.strip():
        raise ValueError("A valid course_id is required")

    # Validate learner IDs present in quiz results
    result_learner_ids = set()

    for result in quiz_results:
        if not isinstance(result, dict):
            raise ValueError("Each quiz result must be a dictionary")

        result_id = result.get("learner_id")

        if result_id is not None:
            if not isinstance(result_id, str) or not result_id.strip():
                raise ValueError("Invalid learner_id in quiz result")
            result_learner_ids.add(result_id)

    if len(result_learner_ids) > 1:
        raise ValueError("Quiz results contain multiple learner IDs")

    if learner_id is not None:
        if not isinstance(learner_id, str) or not learner_id.strip():
            raise ValueError("Invalid learner_id")

        if result_learner_ids and learner_id not in result_learner_ids:
            raise ValueError("Provided learner_id does not match quiz results")

    elif result_learner_ids:
        learner_id = next(iter(result_learner_ids))

    else:
        raise ValueError(
            "learner_id is required when quiz results contain no learner ID"
        )

    # Step 1: Performance analysis
    performance = analyze_performance(quiz_results)

    # Step 2: Calculate topic-wise mastery
    mastery = build_mastery(quiz_results, course_id=course_id)

    # Step 3: Identify knowledge gaps
    knowledge_gaps = identify_knowledge_gaps(mastery)

    # Step 4: Combine all results
    return {
        "learner_id": learner_id,
        "course": course_id,
        "mastery": mastery,
        **knowledge_gaps,
        "performance": performance
    }
