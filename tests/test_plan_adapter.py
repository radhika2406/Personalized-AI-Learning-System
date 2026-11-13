"""Unit tests for the plan adapter module.

Verifies two-way translation between AI engine JSON and backend/frontend formats.
"""

import unittest
from ai_engine.recommendation.plan_adapter import (
    from_backend_format,
    to_frontend_format,
)


class TestPlanAdapter(unittest.TestCase):
    """Test from_backend_format and to_frontend_format adapters."""

    def test_from_backend_format(self):
        """Translate backend LearnerProfile and TopicMastery records into standard analysis."""
        backend_profile = {
            "id": 1,
            "user_id": 42,
            "daily_study_minutes": 45,
            "current_level": "beginner",
            "learning_goal": "Learn Python for data science",
            "course_id": 1,
        }
        backend_masteries = [
            {"topic_id": "variables", "mastery_score": 85.0},
            {"topic_id": "loops", "mastery_score": 33.0},
        ]

        analysis = from_backend_format(backend_profile, backend_masteries)

        self.assertEqual(analysis["learner_id"], "42")
        self.assertEqual(analysis["daily_minutes"], 45)
        self.assertEqual(analysis["topics"]["variables"]["score"], 85.0)
        self.assertEqual(analysis["topics"]["loops"]["score"], 33.0)

    def test_to_frontend_format(self):
        """Translate our study-plan JSON into frontend recommendation card objects."""
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

        frontend_cards = to_frontend_format(our_plan, course_id=1)

        self.assertEqual(len(frontend_cards), 2)

        first_card = frontend_cards[0]
        self.assertEqual(first_card["user_id"], 42)
        self.assertEqual(first_card["course_id"], 1)
        self.assertEqual(first_card["recommendation_type"], "quiz_performance")
        self.assertIn("Revise Topic", first_card["title"])
        self.assertEqual(first_card["priority"], 3)
        self.assertEqual(first_card["status"], "pending")
        self.assertIn("Revise conditions key points", first_card["reason"])

        second_card = frontend_cards[1]
        self.assertEqual(second_card["priority"], 4)  # relearn is priority 4 (urgent)
        self.assertIn("Relearn Topic", second_card["title"])


if __name__ == "__main__":
    unittest.main()
