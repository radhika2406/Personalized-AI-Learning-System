
"""Unit tests for the plan adapter module."""

import unittest

from ai_engine.recommendation.plan_adapter import (
    from_backend_format,
    to_frontend_format,
)


class TestPlanAdapter(unittest.TestCase):

    def test_from_backend_format(self):
        backend_profile = {
            "id": 1,
            "user_id": 42,
            "daily_study_minutes": 45,
            "current_level": "beginner",
            "learning_goal": "Learn Python for data science",
            "course_id": 13,
        }

        backend_masteries = [
            {"topic_id": "variables", "mastery_score": 85.0},
            {"topic_id": "loops", "mastery_score": 33.0},
        ]

        analysis = from_backend_format(
            backend_profile,
            backend_masteries,
        )

        self.assertEqual(analysis["learner_id"], "42")
        self.assertEqual(analysis["daily_minutes"], 45)
        self.assertEqual(
            analysis["topics"]["variables"]["score"], 85.0
        )
        self.assertEqual(
            analysis["topics"]["loops"]["score"], 33.0
        )

    def test_from_backend_format_with_database_ids(self):
        backend_profile = {
            "user_id": 42,
            "daily_study_minutes": 45,
        }

        backend_masteries = [
            {"topic_id": 181, "mastery_score": 85.0},
            {"topic_id": 183, "mastery_score": 33.0},
        ]

        database_to_ai_map = {
            181: "variables",
            182: "conditions",
            183: "loops",
        }

        analysis = from_backend_format(
            backend_profile,
            backend_masteries,
            backend_topic_id_map=database_to_ai_map,
        )

        self.assertEqual(
            analysis["topics"]["variables"]["score"], 85.0
        )
        self.assertEqual(
            analysis["topics"]["loops"]["score"], 33.0
        )

    def test_from_backend_format_with_source_topic_id(self):
        backend_masteries = [
            {
                "topic_id": 181,
                "source_topic_id": "variables",
                "mastery_score": 85.0,
            }
        ]

        analysis = from_backend_format(
            {"user_id": 42},
            backend_masteries,
        )

        self.assertEqual(
            analysis["topics"]["variables"]["score"], 85.0
        )

    def test_missing_backend_topic_mapping_is_rejected(self):
        with self.assertRaises(ValueError):
            from_backend_format(
                {"user_id": 42},
                [{"topic_id": 181, "mastery_score": 85.0}],
            )

    def test_to_frontend_format(self):
        our_plan = {
            "learner_id": "42",
            "daily_minutes": 60,
            "total_minutes": 55,
            "recommended_topics": [
                {
                    "topic": "conditions",
                    "activity": "revise",
                    "minutes": 25,
                    "reason": "Revise conditions key points.",
                },
                {
                    "topic": "loops",
                    "activity": "relearn",
                    "minutes": 30,
                    "reason": "Relearn loops from core principles.",
                },
            ],
            "reason": "Overall plan explanation.",
        }

        ai_to_database_map = {
            "conditions": 182,
            "loops": 183,
        }

        frontend_cards = to_frontend_format(
            our_plan,
            course_id=13,
            topic_id_map=ai_to_database_map,
        )

        self.assertEqual(len(frontend_cards), 2)

        first_card = frontend_cards[0]
        self.assertEqual(first_card["user_id"], 42)
        self.assertEqual(first_card["course_id"], 13)
        self.assertEqual(first_card["topic_id"], 182)
        self.assertEqual(
            first_card["recommendation_type"], "quiz_performance"
        )
        self.assertIn("Revise Topic", first_card["title"])
        self.assertEqual(first_card["priority"], 3)
        self.assertEqual(first_card["status"], "pending")
        self.assertIn(
            "Revise conditions key points", first_card["reason"]
        )

        second_card = frontend_cards[1]
        self.assertEqual(second_card["topic_id"], 183)
        self.assertEqual(second_card["priority"], 4)
        self.assertIn("Relearn Topic", second_card["title"])

    def test_missing_reverse_mapping_is_rejected(self):
        plan = {
            "learner_id": "42",
            "recommended_topics": [
                {
                    "topic": "variables",
                    "activity": "revise",
                    "minutes": 20,
                }
            ],
        }

        with self.assertRaises(ValueError):
            to_frontend_format(plan, course_id=13)

    def test_unknown_topic_is_rejected(self):
        plan = {
            "learner_id": "42",
            "recommended_topics": [
                {
                    "topic": "unknown_topic",
                    "activity": "revise",
                    "minutes": 20,
                }
            ],
        }

        with self.assertRaises(ValueError):
            to_frontend_format(
                plan,
                course_id=13,
                topic_id_map={"variables": 181},
            )


if __name__ == "__main__":
    unittest.main()
