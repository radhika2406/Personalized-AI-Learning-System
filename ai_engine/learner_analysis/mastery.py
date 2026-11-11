"""
mastery.py  (Person A)

Builds the learner's mastery profile across all topics from their quiz results.
"""

from ai_engine.common.schemas import TOPICS


def build_mastery(quiz_results):
    """Build a dictionary mapping each topic to its latest quiz score (or None).

    Parameters:
        quiz_results (list): A list of quiz-result dictionaries (contract 1).

    Returns:
        dict: {topic: score or None} for every topic in schemas.TOPICS.
              A topic never quizzed has score None (never 0).
    """
    if quiz_results is None:
        quiz_results = []

    if not isinstance(quiz_results, list):
        raise TypeError("quiz_results must be a list of dictionaries")

    # Start with all topics set to None (never quizzed / not assessed)
    mastery = {topic: None for topic in TOPICS}
    attempt_numbers = {}

    for result in quiz_results:
        if not isinstance(result, dict):
            raise ValueError("Each quiz result must be a dictionary")

        topic = result.get("topic")
        if topic not in TOPICS:
            raise ValueError(f"Unknown topic: {topic}")

        score = result.get("score_pct")
        attempt = result.get("attempt")

        # Use the most recent attempt for each topic
        if topic in attempt_numbers:
            prev_attempt = attempt_numbers[topic]
            # If attempt numbers are available, keep the higher attempt number
            if attempt is not None and prev_attempt is not None:
                if attempt >= prev_attempt:
                    attempt_numbers[topic] = attempt
                    mastery[topic] = score
            else:
                # Without explicit attempt numbers, later items take precedence
                mastery[topic] = score
        else:
            attempt_numbers[topic] = attempt
            mastery[topic] = score

    return mastery
