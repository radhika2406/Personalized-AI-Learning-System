
"""
test_mastery.py

Tests for latest-attempt and weighted mastery calculation.
"""

import unittest

from ai_engine.common.course_config import list_courses
from assessment.question_management.loader import load_course_topics
from ai_engine.learner_analysis.mastery import build_mastery


COURSE_IDS = list_courses()


def get_topic_id(topic):
    return topic.get("id") or topic.get("topic_id")


class TestBuildMastery(unittest.TestCase):

    def test_no_results(self):
        """All topics should be None when no quiz has been attempted."""

        mastery = build_mastery([], course_id="python")
        topics = load_course_topics("python")
        expected_topics = [get_topic_id(t) for t in topics]

        self.assertEqual(list(mastery.keys()), expected_topics)
        self.assertTrue(all(score is None for score in mastery.values()))

    def test_no_results_none_input(self):
        """None input should return all topics as not assessed."""

        mastery = build_mastery(None, course_id="python")

        self.assertTrue(all(score is None for score in mastery.values()))

    def test_one_topic_only(self):
        """Only the attempted topic should receive a score."""

        results = [
            {
                "learner_id": "S101",
                "course": "python",
                "topic": "loops",
                "score_pct": 75,
                "attempt": 1,
            }
        ]

        mastery = build_mastery(results, course_id="python")

        self.assertEqual(mastery["loops"], 75)

        for topic, score in mastery.items():
            if topic != "loops":
                self.assertIsNone(score)

    def test_two_attempts_same_topic(self):
        """The latest attempt number should determine mastery."""

        results = [
            {
                "course": "python",
                "topic": "loops",
                "score_pct": 40,
                "attempt": 1,
            },
            {
                "course": "python",
                "topic": "loops",
                "score_pct": 85,
                "attempt": 2,
            },
        ]

        mastery = build_mastery(results, course_id="python")

        self.assertEqual(mastery["loops"], 85)

    def test_two_attempts_out_of_order(self):
        """Latest strategy should use the highest attempt number."""

        results = [
            {
                "course": "python",
                "topic": "loops",
                "score_pct": 85,
                "attempt": 2,
            },
            {
                "course": "python",
                "topic": "loops",
                "score_pct": 40,
                "attempt": 1,
            },
        ]

        mastery = build_mastery(results, course_id="python")

        self.assertEqual(mastery["loops"], 85)

    def test_unknown_topic_raises_error(self):
        """A topic that does not belong to the course must be rejected."""

        results = [
            {
                "course": "python",
                "topic": "unknown_topic",
                "score_pct": 50,
                "attempt": 1,
            }
        ]

        with self.assertRaises(ValueError):
            build_mastery(results, course_id="python")

    def test_invalid_input_type(self):
        """Quiz results must be a list."""

        with self.assertRaises(TypeError):
            build_mastery("invalid", course_id="python")

    def test_all_courses_return_all_topics(self):
        """Mastery must support all registered courses."""

        for course_id in COURSE_IDS:
            with self.subTest(course=course_id):

                mastery = build_mastery([], course_id=course_id)
                topics = load_course_topics(course_id)

                expected_topics = [get_topic_id(t) for t in topics]

                self.assertEqual(list(mastery.keys()), expected_topics)

                self.assertTrue(
                    all(score is None for score in mastery.values())
                )

    def test_all_courses_accept_quiz_results(self):
        """The mastery function must work for every registered course."""

        for course_id in COURSE_IDS:
            with self.subTest(course=course_id):

                topics = load_course_topics(course_id)
                topic_id = get_topic_id(topics[0])

                results = [
                    {
                        "learner_id": "S101",
                        "course": course_id,
                        "topic": topic_id,
                        "score_pct": 80,
                        "attempt": 1,
                    }
                ]

                mastery = build_mastery(
                    results,
                    course_id=course_id
                )

                self.assertEqual(mastery[topic_id], 80)
                self.assertEqual(len(mastery), len(topics))


class TestWeightedMastery(unittest.TestCase):

    def test_single_attempt_gets_full_weight(self):
        """A single attempt should retain its original score."""

        results = [
            {
                "course": "python",
                "topic": "loops",
                "score_pct": 75,
                "attempt": 1,
            }
        ]

        mastery = build_mastery(
            results,
            course_id="python",
            strategy="weighted"
        )

        self.assertEqual(mastery["loops"], 75)

    def test_two_attempts_use_40_60_weights(self):
        """Two attempts should use 40% older and 60% newer."""

        results = [
            {
                "course": "python",
                "topic": "loops",
                "score_pct": 40,
                "attempt": 1,
            },
            {
                "course": "python",
                "topic": "loops",
                "score_pct": 90,
                "attempt": 2,
            },
        ]

        mastery = build_mastery(
            results,
            course_id="python",
            strategy="weighted"
        )

        # (40 * 0.4) + (90 * 0.6) = 70
        self.assertEqual(mastery["loops"], 70)

    def test_three_attempts_use_20_30_50_weights(self):
        """Three attempts should use 20%, 30%, and 50%."""

        results = [
            {
                "course": "python",
                "topic": "loops",
                "score_pct": 40,
                "attempt": 1,
            },
            {
                "course": "python",
                "topic": "loops",
                "score_pct": 60,
                "attempt": 2,
            },
            {
                "course": "python",
                "topic": "loops",
                "score_pct": 90,
                "attempt": 3,
            },
        ]

        mastery = build_mastery(
            results,
            course_id="python",
            strategy="weighted"
        )

        # (40 * 0.2) + (60 * 0.3) + (90 * 0.5) = 71
        self.assertEqual(mastery["loops"], 71)

    def test_only_three_most_recent_attempts_are_used(self):
        """Attempts older than the latest three should be ignored."""

        results = [
            {
                "course": "python",
                "topic": "loops",
                "score_pct": 10,
                "attempt": 1,
            },
            {
                "course": "python",
                "topic": "loops",
                "score_pct": 20,
                "attempt": 2,
            },
            {
                "course": "python",
                "topic": "loops",
                "score_pct": 60,
                "attempt": 3,
            },
            {
                "course": "python",
                "topic": "loops",
                "score_pct": 100,
                "attempt": 4,
            },
        ]

        mastery = build_mastery(
            results,
            course_id="python",
            strategy="weighted"
        )

        # (20 * 0.2) + (60 * 0.3) + (100 * 0.5) = 72
        self.assertEqual(mastery["loops"], 72)

    def test_weighted_strategy_handles_out_of_order_results(self):
        """Attempt numbers determine order, not input order."""

        results = [
            {
                "course": "python",
                "topic": "loops",
                "score_pct": 90,
                "attempt": 3,
            },
            {
                "course": "python",
                "topic": "loops",
                "score_pct": 40,
                "attempt": 1,
            },
            {
                "course": "python",
                "topic": "loops",
                "score_pct": 60,
                "attempt": 2,
            },
        ]

        mastery = build_mastery(
            results,
            course_id="python",
            strategy="weighted"
        )

        self.assertEqual(mastery["loops"], 71)

    def test_unassessed_topics_remain_none(self):
        """Topics without attempts should remain not assessed."""

        results = [
            {
                "course": "python",
                "topic": "loops",
                "score_pct": 80,
                "attempt": 1,
            }
        ]

        mastery = build_mastery(
            results,
            course_id="python",
            strategy="weighted"
        )

        self.assertEqual(mastery["loops"], 80)

        self.assertIsNone(mastery["variables"])
        self.assertIsNone(mastery["functions"])

    def test_weighted_strategy_uses_input_order_without_attempt_numbers(self):
        """Input order is used when attempt numbers are unavailable."""

        results = [
            {
                "course": "python",
                "topic": "loops",
                "score_pct": 40,
            },
            {
                "course": "python",
                "topic": "loops",
                "score_pct": 90,
            },
        ]

        mastery = build_mastery(
            results,
            course_id="python",
            strategy="weighted"
        )

        self.assertEqual(mastery["loops"], 70)

    def test_mixed_attempt_number_formats_are_rejected(self):
        """Mixed numbered and unnumbered attempts are ambiguous."""

        results = [
            {
                "course": "python",
                "topic": "loops",
                "score_pct": 40,
                "attempt": 1,
            },
            {
                "course": "python",
                "topic": "loops",
                "score_pct": 90,
            },
        ]

        with self.assertRaises(ValueError):
            build_mastery(
                results,
                course_id="python",
                strategy="weighted"
            )

    def test_invalid_strategy_is_rejected(self):
        """Unknown mastery strategies should raise ValueError."""

        with self.assertRaises(ValueError):
            build_mastery(
                [],
                course_id="python",
                strategy="average"
            )


if __name__ == "__main__":
    unittest.main()
