
"""
mastery.py

Builds a learner's topic-wise mastery profile
for any registered course.

Supported strategies:
- latest: Uses the latest attempt for each topic (default).
- weighted: Uses the three most recent attempts with
  greater importance given to recent performance.

Each topic receives:
- A score from 0 to 100, if assessed.
- None, if not assessed yet.
"""

from ai_engine.common.course_config import get_course
from assessment.question_management.loader import load_course_topics


def build_mastery(quiz_results, course_id=None, strategy="latest"):
    """
    Build a mastery dictionary for the selected course.

    Parameters:
        quiz_results:
            List of quiz-result dictionaries (Contract 1).

        course_id:
            Selected course identifier.
            If omitted, inferred from quiz results.
            Defaults to Python for an empty result list.

        strategy:
            "latest"   - Uses the latest attempt (default).
            "weighted" - Uses the three most recent attempts.

    Returns:
        Dictionary mapping topic IDs to scores or None.
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

    # Validate strategy
    if strategy not in ("latest", "weighted"):
        raise ValueError(
            "strategy must be either 'latest' or 'weighted'"
        )

    # Use weighted recalibration when requested
    if strategy == "weighted":
        return _build_weighted_mastery(
            quiz_results,
            course_id,
            topic_ids
        )

    # Default strategy: latest attempt
    mastery = {
        topic_id: None
        for topic_id in topic_ids
    }

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


def _build_weighted_mastery(quiz_results, course_id, topic_ids):
    """
    Calculate mastery using the three most recent attempts.

    Weights:
        1 attempt: 100%
        2 attempts: 40%, 60%
        3 or more attempts: 20%, 30%, 50%

    If attempt numbers are unavailable, input order is used.

    Mixed numbered and unnumbered attempts for the same
    topic are rejected because their chronological order
    cannot be determined reliably.
    """

    mastery = {
        topic_id: None
        for topic_id in topic_ids
    }

    grouped_results = {
        topic_id: []
        for topic_id in topic_ids
    }

    # Validate and group quiz results by topic
    for index, result in enumerate(quiz_results):

        result_course = result.get("course")

        if (
            result_course is not None
            and result_course != course_id
        ):
            raise ValueError(
                f"Quiz result belongs to '{result_course}', "
                f"but selected course is '{course_id}'"
            )

        topic = result.get("topic")

        if topic not in grouped_results:
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

        # Validate attempt number
        if attempt is not None:
            if (
                isinstance(attempt, bool)
                or not isinstance(attempt, int)
                or attempt < 1
            ):
                raise ValueError(
                    f"Invalid attempt number for topic '{topic}'"
                )

        grouped_results[topic].append({
            "score": score,
            "attempt": attempt,
            "index": index
        })

    # Calculate weighted mastery for each assessed topic
    for topic, attempts in grouped_results.items():

        if not attempts:
            continue

        has_numbered = any(
            item["attempt"] is not None
            for item in attempts
        )

        has_unnumbered = any(
            item["attempt"] is None
            for item in attempts
        )

        if has_numbered and has_unnumbered:
            raise ValueError(
                f"Topic '{topic}' contains mixed numbered "
                "and unnumbered attempts"
            )

        # Determine chronological order
        if has_numbered:
            attempts.sort(
                key=lambda item: (
                    item["attempt"],
                    item["index"]
                )
            )
        else:
            attempts.sort(
                key=lambda item: item["index"]
            )

        # Keep only the three most recent attempts
        recent_attempts = attempts[-3:]
        count = len(recent_attempts)

        # Assign weights
        if count == 1:
            weights = [1.0]
        elif count == 2:
            weights = [0.4, 0.6]
        else:
            weights = [0.2, 0.3, 0.5]

        # Calculate weighted score
        weighted_score = sum(
            item["score"] * weight
            for item, weight in zip(recent_attempts, weights)
        )

        mastery[topic] = round(weighted_score, 2)

    return mastery
