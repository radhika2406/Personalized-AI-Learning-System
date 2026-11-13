"""Unit tests for the study planner.

Verifies budget invariants, time allocations, reason generation,
and plans for all 8 test learners.
"""

import json
from pathlib import Path
import unittest

from ai_engine.recommendation.study_planner import build_plan


class TestStudyPlanner(unittest.TestCase):
    """Test study_planner.build_plan across all 8 test learners."""

    @classmethod
    def setUpClass(cls):
        cls.learners_dir = Path(__file__).resolve().parent / "test_learners"

    def _load_learner(self, filename: str) -> dict:
        filepath = self.learners_dir / filename
        with open(filepath, mode="r", encoding="utf-8") as f:
            return json.load(f)

    def test_all_eight_learners_invariants(self):
        """Verify budget and summation invariants across all 8 test learners."""
        filenames = [
            "learner_all_weak.json",
            "learner_all_strong.json",
            "learner_mixed.json",
            "learner_nothing_assessed.json",
            "learner_budget_30.json",
            "learner_budget_90.json",
            "learner_one_weak.json",
            "learner_prereq_gap.json",
        ]

        for fname in filenames:
            with self.subTest(learner=fname):
                data = self._load_learner(fname)
                plan = build_plan(data)

                # Basic contract shape
                self.assertIn("learner_id", plan)
                self.assertIn("daily_minutes", plan)
                self.assertIn("total_minutes", plan)
                self.assertIn("recommended_topics", plan)
                self.assertIn("reason", plan)
                self.assertIsInstance(plan["reason"], str)
                self.assertTrue(len(plan["reason"]) > 0)

                # Invariant 1: total_minutes <= daily_minutes
                self.assertLessEqual(
                    plan["total_minutes"],
                    plan["daily_minutes"],
                    f"total_minutes exceeded daily_minutes for {fname}",
                )

                # Invariant 2: total_minutes == sum of topic minutes
                expected_sum = sum(t["minutes"] for t in plan["recommended_topics"])
                self.assertEqual(
                    plan["total_minutes"],
                    expected_sum,
                    f"total_minutes does not match sum of topic minutes for {fname}",
                )

                # Each topic has required fields
                for t in plan["recommended_topics"]:
                    self.assertIn("topic", t)
                    self.assertIn("activity", t)
                    self.assertIn("minutes", t)
                    self.assertIn("reason", t)
                    self.assertGreaterEqual(t["minutes"], 10)

    def test_different_budgets_yield_different_plans(self):
        """The 30-minute and 90-minute learners must receive different plans."""
        data_30 = self._load_learner("learner_budget_30.json")
        data_90 = self._load_learner("learner_budget_90.json")

        plan_30 = build_plan(data_30)
        plan_90 = build_plan(data_90)

        self.assertNotEqual(plan_30["total_minutes"], plan_90["total_minutes"])
        self.assertNotEqual(len(plan_30["recommended_topics"]), len(plan_90["recommended_topics"]))

    def test_nothing_assessed_no_crash(self):
        """Learner with nothing assessed safely receives assess first topics."""
        data = self._load_learner("learner_nothing_assessed.json")
        plan = build_plan(data)

        self.assertGreater(len(plan["recommended_topics"]), 0)
        for t in plan["recommended_topics"]:
            self.assertEqual(t["activity"], "assess first")
        # Ensure reason does not say 0%
        self.assertNotIn("0%", plan["reason"])

    def test_very_low_budget_edge_cases(self):
        """5 minutes (below min threshold) and 10 minutes edge cases."""
        # 5 minutes: below 10 min minimum
        plan_5 = build_plan({"learner_id": "test_5", "daily_minutes": 5, "topics": {}})
        self.assertEqual(plan_5["total_minutes"], 0)
        self.assertEqual(len(plan_5["recommended_topics"]), 0)
        self.assertIn("below the minimum", plan_5["reason"])

        # 10 minutes: exactly 1 topic allocated 10 minutes
        plan_10 = build_plan({"learner_id": "test_10", "daily_minutes": 10, "topics": {}})
        self.assertEqual(plan_10["total_minutes"], 10)
        self.assertEqual(len(plan_10["recommended_topics"]), 1)
        self.assertEqual(plan_10["recommended_topics"][0]["minutes"], 10)


if __name__ == "__main__":
    unittest.main()
