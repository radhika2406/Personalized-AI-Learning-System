
"""
score_quiz.py (Person A)

Scores a quiz for any course registered in course_config.py.

The selected course_id determines which questions and topics are used.
No course-specific scoring logic is required.
"""

from ai_engine.common.schemas import ANSWER_CHOICES
from ai_engine.common.course_config import get_course
from assessment.question_management.loader import (
    load_course_questions,
    load_course_topics,
)


def load_questions(course_id="python"):
    """
    Load all questions for the selected course.

    Returns:
        Dictionary: {question_id: question_details}
    """
    if not get_course(course_id):
        raise ValueError(f"Unknown course: {course_id}")

    return load_course_questions(course_id)


def score_quiz(
    learner_id,
    topic,
    answers,
    questions,
    attempt=1,
    course_id="python",
):
    """
    Evaluate a learner's quiz for any registered course.

    Args:
        learner_id: Unique learner identifier.
        topic: Topic ID being tested.
        answers: {question_id: selected_answer}
        questions: Question dictionary for the selected course.
        attempt: Attempt number.
        course_id: Selected course identifier.

    Returns:
        Quiz result dictionary (Contract 1).
    """

    # Validate learner
    if not isinstance(learner_id, str) or not learner_id.strip():
        raise ValueError("learner_id is missing")

    # Validate course
    if not get_course(course_id):
        raise ValueError(f"Unknown course: {course_id}")

    # Validate topic against the selected course
    course_topics = load_course_topics(course_id)
    valid_topic_ids = {
        item.get("id") or item.get("topic_id")
        for item in course_topics
    }

    if topic not in valid_topic_ids:
        raise ValueError(
            f"Unknown topic '{topic}' for course '{course_id}'"
        )

    # Validate answers and question dictionary
    if not isinstance(answers, dict) or not answers:
        raise ValueError("No answers submitted")

    if not isinstance(questions, dict):
        raise ValueError("questions must be a dictionary")

    if isinstance(attempt, bool) or not isinstance(attempt, int) or attempt < 1:
        raise ValueError("attempt must be a whole number of 1 or more")

    correct_count = 0
    wrong_question_ids = []

    for question_id, chosen_answer in answers.items():

        question = questions.get(question_id)

        if question is None:
            raise ValueError(
                f"Unknown question for this course: {question_id}"
            )

        question_topic = (
            question.get("topic")
            or question.get("topic_id")
        )

        if question_topic != topic:
            raise ValueError(
                f"Question '{question_id}' does not belong to topic '{topic}'"
            )

        # Skipped answers count as wrong
        if chosen_answer is None or str(chosen_answer).strip() == "":
            wrong_question_ids.append(question_id)
            continue

        answer = str(chosen_answer).strip().lower()

        if answer not in ANSWER_CHOICES:
            raise ValueError(
                f"Answer for {question_id} must be a, b, c or d"
            )

        correct_answer = str(
            question.get("correct", "")
        ).strip().lower()

        if correct_answer not in ANSWER_CHOICES:
            raise ValueError(
                f"Question '{question_id}' has an invalid correct answer"
            )

        if answer == correct_answer:
            correct_count += 1
        else:
            wrong_question_ids.append(question_id)

    total_questions = len(answers)
    score_percentage = round(
        (correct_count / total_questions) * 100
    )

    return {
        "learner_id": learner_id,
        "course": course_id,
        "topic": topic,
        "score_pct": score_percentage,
        "correct": correct_count,
        "total": total_questions,
        "attempt": attempt,
        "wrong_question_ids": wrong_question_ids,
    }
