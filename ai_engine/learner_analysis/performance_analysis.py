
"""
performance_analysis.py

Analyzes a learner's quiz performance.

Quiz results must be supplied in chronological order
(oldest first, newest last) for score_trend and improvement.
"""


def analyze_performance(quiz_results):
    """
    Calculate overall and topic-wise performance.

    Returns:
        total_quizzes
        average_score
        overall_accuracy
        total_correct
        total_questions
        total_incorrect
        topic_performance
        score_trend
        improvement
    """

    if not isinstance(quiz_results, list):
        raise ValueError("quiz_results must be a list")

    if not quiz_results:
        return {
            "total_quizzes": 0,
            "average_score": None,
            "overall_accuracy": None,
            "total_correct": 0,
            "total_questions": 0,
            "total_incorrect": 0,
            "topic_performance": {},
            "score_trend": [],
            "improvement": None
        }

    total_correct = 0
    total_questions = 0
    scores = []
    topic_performance = {}

    for result in quiz_results:

        if not isinstance(result, dict):
            raise ValueError("Each quiz result must be a dictionary")

        required = ["topic", "score_pct", "correct", "total"]

        for field in required:
            if field not in result:
                raise ValueError(f"Missing field: {field}")

        topic = result["topic"]
        score = result["score_pct"]
        correct = result["correct"]
        total = result["total"]

        if not isinstance(topic, str) or not topic.strip():
            raise ValueError("Invalid topic")

        if (
            isinstance(score, bool)
            or not isinstance(score, (int, float))
            or not 0 <= score <= 100
        ):
            raise ValueError("Invalid score_pct")

        if (
            isinstance(correct, bool)
            or not isinstance(correct, int)
            or isinstance(total, bool)
            or not isinstance(total, int)
            or total <= 0
            or correct < 0
            or correct > total
        ):
            raise ValueError("Invalid correct or total value")

        # Verify that the percentage matches the quiz result.
        expected_score = round((correct / total) * 100)

        if score != expected_score:
            raise ValueError(
            "score_pct does not match correct and total"
        )

        total_correct += correct
        total_questions += total
        scores.append(score)

        if topic not in topic_performance:
            topic_performance[topic] = {
                "attempts": 0,
                "total_score": 0,
                "average_score": 0
            }

        topic_performance[topic]["attempts"] += 1
        topic_performance[topic]["total_score"] += score

    for topic, data in topic_performance.items():
        data["average_score"] = round(
            data["total_score"] / data["attempts"], 2
        )
        del data["total_score"]

    average_score = round(sum(scores) / len(scores), 2)

    overall_accuracy = round(
        (total_correct / total_questions) * 100, 2
    )

    improvement = (
        round(scores[-1] - scores[0], 2)
        if len(scores) > 1
        else None
    )

    return {
        "total_quizzes": len(quiz_results),
        "average_score": average_score,
        "overall_accuracy": overall_accuracy,
        "total_correct": total_correct,
        "total_questions": total_questions,
        "total_incorrect": total_questions - total_correct,
        "topic_performance": topic_performance,
        "score_trend": scores,
        "improvement": improvement
    }
