
"""Tests for the adaptive learning engine."""

import copy
import json
from pathlib import Path
import unittest

from ai_engine.recommendation.adaptive_learning import adapt_plan


def simulate_quiz_result(
    analysis: dict,
    topic_id: str,
    new_score: float | int | None,
) -> dict:
    """Simulate a new quiz result using the existing mastery structure."""
    updated = copy.deepcopy(analysis)

    if "mastery" not in updated or not isinstance(updated["mastery"], dict):
        updated["mastery"] = {}

    updated["mastery"][topic_id] = new_score
    return updated


class TestAdaptiveLearning(unittest.TestCase):
    """Test adaptive plan updates after new quiz results."""

    @classmethod
    def setUpClass(cls):
        cls.learners_dir = Path(__file__).resolve().parent / "test_learners"

    def _load_learner(self, filename: str) -> dict:
        filepath = self.learners_dir / filename
        with open(filepath, mode="r", encoding="utf-8") as file:
            return json.load(file)

    def test_case_1_weak_topic_becomes_strong(self):
        """A weak topic should be updated after the learner improves."""
        before = self._load_learner("learner_one_weak.json")

        self.assertEqual(before["mastery"]["loops"], 25)

        after = simulate_quiz_result(before, "loops", 90)
        result = adapt_plan(before, after)

        self.assertIn("plan", result)
        self.assertIn("changes", result)
        self.assertIsInstance(result["plan"], dict)
        self.assertIsInstance(result["changes"], list)

    def test_case_2_not_assessed_topic_gets_first_score(self):
        """A topic should be updated when it receives its first score."""
        before = self._load_learner("learner_nothing_assessed.json")

        after = simulate_quiz_result(before, "variables", 65)
        result = adapt_plan(before, after)

        self.assertIsInstance(result["plan"], dict)
        self.assertIsInstance(result["changes"], list)

        self.assertTrue(
            any("variables" in change for change in result["changes"])
        )

    def test_case_3_topic_performance_drops(self):
        """A topic's recommendation should adapt when its score drops."""
        before = self._load_learner("learner_mixed.json")

        # In the canonical fixture, dictionaries has a score of 75.
        self.assertEqual(before["mastery"]["dictionaries"], 75)

        after = simulate_quiz_result(before, "dictionaries", 25)
        result = adapt_plan(before, after)

        self.assertIsInstance(result["plan"], dict)
        self.assertIsInstance(result["changes"], list)

        self.assertTrue(
            any("dictionaries" in change for change in result["changes"])
        )

    def test_case_4_prerequisite_unlocks_next_topic(self):
        """Improving a prerequisite should allow a dependent topic to be recommended."""
        before = self._load_learner("learner_prereq_gap.json")

        self.assertIsNone(before["mastery"]["conditions"])

        after = simulate_quiz_result(before, "conditions", 78)
        result = adapt_plan(before, after)

        self.assertIsInstance(result["plan"], dict)
        self.assertIsInstance(result["changes"], list)

        self.assertTrue(
            any(
                "conditions" in change or "loops" in change
                for change in result["changes"]
            )
        )


if __name__ == "__main__":
    unittest.main()
