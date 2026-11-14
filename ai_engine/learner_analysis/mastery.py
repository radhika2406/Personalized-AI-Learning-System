
"""
mastery.py 

Builds a learner's topic-wise mastery profile
for any registered course.

Each topic receives:
- A score from 0 to 100, if assessed.
- None, if not assessed yet.

The latest attempt number is used when multiple
quiz results exist for the same topic.
"""

from ai_engine.common.course_config import get_course
from assessment.question_management.loader import load_course_topics


def build_mastery(quiz_results, course_id=None):
    """
    Build a mastery dictionary for the selected course.

    Parameters:
        quiz_results:
            List of quiz-result dictionaries (Contract 1).

        course_id:
            Selected course identifier, such as:
            python, java, cpp, machine_learning, dbms.

            If omitted, the course is inferred from quiz results.
            For an empty result list, Python is retained as the
            backward-compatible default. Production code should
            always pass course_id explicitly.

    Returns:
        Dictionary:
        {
            "topic_1": 85,
            "topic_2": None,
            "topic_3": 45
        }
    """

    # Validate input
    if quiz_results is None:
        quiz_results = []

    if not isinstance(quiz_results, list):
        raise TypeError("quiz_results must be a list of dictionaries")

    for result in quiz_results:
        if not isinstance(result, dict):
            raise ValueError(
                "Each quiz result must be a dictionary"
            )

    # Infer course when it is not explicitly supplied
    if course_id is None:
        result_courses = {
            result.get("course")
            for result in quiz_results
            if result.get("course") is not None
        }

        if len(result_courses) > 1:
            raise ValueError(
                "Quiz results contain multiple courses. "
                "Pass course_id explicitly."
            )

        if len(result_courses) == 1:
            course_id = result_courses.pop()
        else:
            # Backward compatibility for existing Python tests
            course_id = "python"

    # Validate selected course
    if not get_course(course_id):
        raise ValueError(f"Unknown course: {course_id}")

    # Load all topics belonging to this course
    course_topics = load_course_topics(course_id)

    topic_ids = [
        topic.get("id") or topic.get("topic_id")
        for topic in course_topics
    ]

    # Every topic starts as not assessed
    mastery = {
        topic_id: None
        for topic_id in topic_ids
    }

    # Track the latest attempt for each topic
    latest_attempts = {
        topic_id: None
        for topic_id in topic_ids
    }

    for result in quiz_results:

        result_course = result.get("course")

        # Prevent mixing results from different courses
        if (
            result_course is not None
            and result_course != course_id
        ):
            raise ValueError(
                f"Quiz result belongs to '{result_course}', "
                f"but selected course is '{course_id}'"
            )

        topic = result.get("topic")

        if topic not in mastery:
            raise ValueError(
                f"Unknown topic '{topic}' for course '{course_id}'"
            )

        score = result.get("score_pct")
        attempt = result.get("attempt")

        # Validate score
        if (
            isinstance(score, bool)
            or not isinstance(score, (int, float))
            or not 0 <= score <= 100
        ):
            raise ValueError(
                f"Invalid score for topic '{topic}': {score}"
            )

        # Validate attempt number when provided
        if attempt is not None:
            if (
                isinstance(attempt, bool)
                or not isinstance(attempt, int)
                or attempt < 1
            ):
                raise ValueError(
                    f"Invalid attempt number for topic '{topic}'"
                )

        previous_attempt = latest_attempts[topic]

        # First result for this topic
        if previous_attempt is None and mastery[topic] is None:
            latest_attempts[topic] = attempt
            mastery[topic] = score
            continue

        # Both attempts have numbers:
        # retain the result with the higher attempt number
        if attempt is not None and previous_attempt is not None:
            if attempt >= previous_attempt:
                latest_attempts[topic] = attempt
                mastery[topic] = score

        # If attempt numbers are unavailable,
        # the later result takes precedence
        elif attempt is None and previous_attempt is None:
            mastery[topic] = score

        # A numbered attempt is more reliable than
        # a result without an attempt number
        elif attempt is not None and previous_attempt is None:
            latest_attempts[topic] = attempt
            mastery[topic] = score

    return mastery
