
"""
progress_tracking.py

Builds a learner's overall course progress report.

A topic is considered completed only when its mastery
score is 80% or higher.

Unassessed topics remain separate from incomplete topics.
"""

from ai_engine.common.course_config import get_course
from ai_engine.common.schemas import mastery_level
from assessment.question_management.loader import load_course_topics

from ai_engine.learner_analysis.analysis_pipeline import analyze_learner
from assessment.scoring.exam_manager import STAGE_METADATA


COMPLETION_THRESHOLD = 80


def _build_exam_progress(exam_history, course_id, learner_id):
    """Summarize examination progress for the selected learner and course."""

    if exam_history is None:
        exam_history = []

    if not isinstance(exam_history, list):
        raise ValueError("exam_history must be a list")

    stages = {}

    for stage in STAGE_METADATA:
        stages[stage] = {
            "stage": stage,
            "stage_name": STAGE_METADATA[stage]["name"],
            "status": "pending",
            "attempts": 0,
            "latest_score": None
        }

    for index, record in enumerate(exam_history):

        if not isinstance(record, dict):
            raise ValueError("Each exam history record must be a dictionary")

        # Ignore records belonging to another course or learner.
        record_course = record.get("course_id")
        record_learner = record.get("learner_id")

        if record_course is not None and record_course != course_id:
            continue

        if learner_id is not None and record_learner is not None:
            if record_learner != learner_id:
                continue

        stage = record.get("stage")

        if stage not in STAGE_METADATA:
            raise ValueError(f"Unknown examination stage: {stage}")

        completion_status = record.get("completion_status")

        if completion_status not in ("passed", "failed"):
            raise ValueError(
                f"Invalid completion status for stage '{stage}'"
            )

        score = record.get("score")

        if (
            isinstance(score, bool)
            or not isinstance(score, (int, float))
            or not 0 <= score <= 100
        ):
            raise ValueError(
                f"Invalid examination score for stage '{stage}'"
            )

        attempt_number = record.get("attempt_number", index + 1)

        if (
            isinstance(attempt_number, bool)
            or not isinstance(attempt_number, int)
            or attempt_number < 1
        ):
            raise ValueError("Invalid examination attempt number")

        stage_data = stages[stage]
        stage_data["attempts"] += 1

        # Keep the score from the highest attempt number.
        previous_attempt = stage_data.get("_latest_attempt", 0)

        if attempt_number >= previous_attempt:
            stage_data["latest_score"] = score
            stage_data["_latest_attempt"] = attempt_number

        # A stage remains passed once it has been passed.
        if completion_status == "passed":
            stage_data["status"] = "passed"
        elif stage_data["status"] != "passed":
            stage_data["status"] = "failed"

    for stage_data in stages.values():
        stage_data.pop("_latest_attempt", None)

    stage_list = list(stages.values())

    passed_count = sum(
        stage["status"] == "passed"
        for stage in stage_list
    )

    return {
        "total_stages": len(stage_list),
        "passed_stages": passed_count,
        "pending_stages": len(stage_list) - passed_count,
        "stages": stage_list
    }


def build_progress_report(
    quiz_results,
    course_id,
    learner_id=None,
    exam_history=None
):
    """
    Generate an overall progress report for one learner.

    Parameters:
        quiz_results:
            List of quiz-result dictionaries.

        course_id:
            Selected course identifier.

        learner_id:
            Learner identifier. Required for empty quiz results.

        exam_history:
            Optional list of examination attempt records.

    Returns:
        Dictionary containing course, topic, quiz and exam progress.
    """

    if not isinstance(quiz_results, list):
        raise ValueError("quiz_results must be a list")

    if not isinstance(course_id, str) or not course_id.strip():
        raise ValueError("A valid course_id is required")

    if not get_course(course_id):
        raise ValueError(f"Unknown course: {course_id}")

    if learner_id is not None:
        if not isinstance(learner_id, str) or not learner_id.strip():
            raise ValueError("Invalid learner_id")

    # Reuse the existing learner-analysis pipeline.
    analysis = analyze_learner(
        quiz_results,
        course_id,
        learner_id=learner_id
    )

    learner_id = analysis["learner_id"]

    topics = load_course_topics(course_id)
    mastery = analysis["mastery"]

    topic_progress = {}

    completed_topics = []
    assessed_topics = []
    unassessed_topics = []

    for topic in topics:

        topic_id = topic.get("id") or topic.get("topic_id")
        topic_name = topic.get("name") or topic.get("title")

        score = mastery[topic_id]
        level = mastery_level(score)

        if score is None:
            status = "not_assessed"
            unassessed_topics.append(topic_id)

        elif score >= COMPLETION_THRESHOLD:
            status = "completed"
            completed_topics.append(topic_id)
            assessed_topics.append(topic_id)

        else:
            status = "in_progress"
            assessed_topics.append(topic_id)

        topic_progress[topic_id] = {
            "topic_name": topic_name,
            "order": topic.get("order"),
            "score": score,
            "mastery_level": level,
            "status": status
        }

    total_topics = len(topics)
    completed_count = len(completed_topics)
    assessed_count = len(assessed_topics)
    unassessed_count = len(unassessed_topics)

    course_progress_pct = round(
        (completed_count / total_topics) * 100, 2
    ) if total_topics else 0

    exam_progress = _build_exam_progress(
        exam_history,
        course_id,
        learner_id
    )

    return {
        "learner_id": learner_id,
        "course_id": course_id,

        "course_progress": {
            "total_topics": total_topics,
            "completed_topics": completed_count,
            "assessed_topics": assessed_count,
            "unassessed_topics": unassessed_count,
            "course_progress_pct": course_progress_pct,
            "completion_threshold": COMPLETION_THRESHOLD,
            "completed_topic_ids": completed_topics,
            "unassessed_topic_ids": unassessed_topics
        },

        "topic_progress": topic_progress,

        "quiz_progress": analysis["performance"],

        "knowledge_gaps": {
            "weak_topics": analysis["weak_topics"],
            "developing_topics": analysis["developing_topics"],
            "good_topics": analysis["good_topics"],
            "strong_topics": analysis["strong_topics"],
            "not_assessed": analysis["not_assessed"]
        },

        "exam_progress": exam_progress
    }
