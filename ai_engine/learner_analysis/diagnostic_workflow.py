
"""
diagnostic_workflow.py

Coordinates the initial diagnostic assessment
and diagnostic report generation.
"""

from assessment.scoring.initial_assessment import (
    generate_initial_assessment,
    evaluate_initial_assessment,
)

from ai_engine.learner_analysis.diagnostic_report import (
    generate_diagnostic_report,
)


def start_diagnostic_assessment(course_id):
    """
    Generate an assessment for the learner to attempt.
    """

    return generate_initial_assessment(course_id)


def submit_diagnostic_assessment(
    learner_id,
    course_id,
    answers,
    assessment,
):
    """
    Evaluate submitted answers and generate the
    learner's diagnostic report.
    """

    assessment_result = evaluate_initial_assessment(
        learner_id=learner_id,
        course_id=course_id,
        answers=answers,
        assessment=assessment,
    )

    diagnostic_report = generate_diagnostic_report(
        assessment_result
    )

    return {
        "assessment_result": assessment_result,
        "diagnostic_report": diagnostic_report,
    }
