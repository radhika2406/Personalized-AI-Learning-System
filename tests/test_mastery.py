'''
"""
test_mastery.py  (Tests for build_mastery by Person A)
"""

import unittest
from ai_engine.common.schemas import TOPICS
from ai_engine.learner_analysis.mastery import build_mastery


class TestBuildMastery(unittest.TestCase):
    def test_no_results(self):
        """When there are no quiz results, every topic should have score None."""
        mastery = build_mastery([])
        self.assertEqual(list(mastery.keys()), TOPICS)
        for topic in TOPICS:
            self.assertIsNone(mastery[topic], f"{topic} should be None when unquizzed")

    def test_no_results_none_input(self):
        """None input should also safely return all topics mapped to None."""
        mastery = build_mastery(None)
        self.assertEqual(list(mastery.keys()), TOPICS)
        for topic in TOPICS:
            self.assertIsNone(mastery[topic])

    def test_one_topic_only(self):
        """When only one topic is quizzed, only that topic has a score, others are None."""
        results = [
            {
                "learner_id": "S101",
                "course": "python",
                "topic": "loops",
                "score_pct": 75,
                "correct": 3,
                "total": 4,
                "attempt": 1,
                "wrong_question_ids": ["loops_q1"],
            }
        ]
        mastery = build_mastery(results)
        self.assertEqual(list(mastery.keys()), TOPICS)
        self.assertEqual(mastery["loops"], 75)
        for topic in TOPICS:
            if topic != "loops":
                self.assertIsNone(mastery[topic], f"{topic} should be None")

    def test_two_attempts_same_topic(self):
        """When a topic has multiple attempts, the most recent attempt's score is used."""
        results = [
            {
                "learner_id": "S101",
                "course": "python",
                "topic": "functions",
                "score_pct": 50,
                "correct": 3,
                "total": 6,
                "attempt": 1,
                "wrong_question_ids": ["functions_q1", "functions_q2", "functions_q3"],
            },
            {
                "learner_id": "S101",
                "course": "python",
                "topic": "functions",
                "score_pct": 83,
                "correct": 5,
                "total": 6,
                "attempt": 2,
                "wrong_question_ids": ["functions_q1"],
            },
        ]
        mastery = build_mastery(results)
        self.assertEqual(mastery["functions"], 83)

    def test_two_attempts_out_of_order(self):
        """Even if results arrive out of order, the higher attempt number is used."""
        results = [
            {
                "learner_id": "S101",
                "course": "python",
                "topic": "lists",
                "score_pct": 90,
                "correct": 9,
                "total": 10,
                "attempt": 2,
                "wrong_question_ids": ["lists_q1"],
            },
            {
                "learner_id": "S101",
                "course": "python",
                "topic": "lists",
                "score_pct": 40,
                "correct": 4,
                "total": 10,
                "attempt": 1,
                "wrong_question_ids": ["lists_q1", "lists_q2", "lists_q3", "lists_q4", "lists_q5", "lists_q6"],
            },
        ]
        mastery = build_mastery(results)
        self.assertEqual(mastery["lists"], 90)

    def test_unknown_topic_raises_error(self):
        """A result with an unknown topic must raise a clear ValueError."""
        results = [
            {
                "learner_id": "S101",
                "course": "python",
                "topic": "data_structures",
                "score_pct": 70,
                "attempt": 1,
            }
        ]
        with self.assertRaises(ValueError) as context:
            build_mastery(results)
        self.assertIn("Unknown topic", str(context.exception))

    def test_invalid_input_type(self):
        """Passing something other than a list or None raises TypeError."""
        with self.assertRaises(TypeError):
            build_mastery("not a list")


if __name__ == "__main__":
    unittest.main()
'''

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
                "correct": 3,
                "total": 4,
                "attempt": 1,
                "wrong_question_ids": ["loops_q1"],
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
        """Results should be ordered by attempt number, not input order."""

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

                self.assertEqual(
                    list(mastery.keys()),
                    expected_topics
                )

                self.assertTrue(
                    all(score is None for score in mastery.values())
                )

    def test_all_courses_accept_quiz_results(self):
        """The same mastery function must work for every course."""

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


if __name__ == "__main__":
    unittest.main()
