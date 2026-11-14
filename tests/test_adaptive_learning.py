"""Unit tests for adaptive learning engine.

Tests before vs after adaptation across 4 core scenarios:
1. Weak topic becomes strong (moves on to next topic)
2. Not-assessed topic gets first score
3. Quiz score drops (topic gets worse)
4. Prerequisite becomes good and unlocks next topic
"""

import copy
import json
from pathlib import Path
import unittest

from ai_engine.recommendation.adaptive_learning import adapt_plan



def simulate_quiz_result(analysis: dict, topic_id: str, new_score: float | int | None) -> dict:
    """Simulate a new quiz result using the existing mastery data structure."""
    updated = copy.deepcopy(analysis)

    if "mastery" not in updated or not isinstance(updated["mastery"], dict):
        updated["mastery"] = {}

    updated["mastery"][topic_id] = new_score
    return updated

class TestAdaptiveLearning(unittest.TestCase):
    """Test adaptive plan updating when a new quiz result arrives."""

    @classmethod
    def setUpClass(cls):
        cls.learners_dir = Path(__file__).resolve().parent / "test_learners"

    def _load_learner(self, filename: str) -> dict:
        filepath = self.learners_dir / filename
        with open(filepath, mode="r", encoding="utf-8") as f:
            return json.load(f)

    def test_case_1_weak_becomes_strong(self):
        """Case 1: Weak topic becomes strong. Activity changes to advance and next topic prioritizes."""
        before = self._load_learner("learner_one_weak.json")
        # In learner_one_weak, loops is at 25% (weak)
        self.assertEqual(before["mastery"]["loops"], 25)

        # Student passes loops quiz with 90% (strong)
        after = simulate_quiz_result(before, "loops", 90)

        result = adapt_plan(before, after)
        new_plan = result["plan"]
        changes = result["changes"]

        # Activity for loops should now be 'advance'
        loops_item = next((t for t in new_plan["recommended_topics"] if t["topic"] == "loops"), None)
        if loops_item:
            self.assertEqual(loops_item["activity"], "advance")

        # Changes list should record the activity change
        self.assertTrue(any("Topic 'loops' activity changed" in c for c in changes))

    def test_case_2_not_assessed_gets_first_score(self):
        """Case 2: Not-assessed topic gets its first score."""
        before = self._load_learner("learner_nothing_assessed.json")

        # Student takes diagnostic assessment on variables and scores 65% (good)
        after = simulate_quiz_result(before, "variables", 65)

        result = adapt_plan(before, after)
        changes = result["changes"]

        # Variables activity should change from 'assess first' to 'practice'
        self.assertTrue(any("Topic 'variables' activity changed from 'assess first' to 'practice'" in c for c in changes))

    def test_case_3_quiz_makes_topic_worse(self):
        """Case 3: Quiz makes a topic worse (good -> weak)."""
        before = self._load_learner("learner_mixed.json")
        # In learner_mixed, functions is 70 (good)
        self.assertEqual(before["mastery"]["functions"], 70)

        # Retake quiz score drops to 25% (weak)
        after = simulate_quiz_result(before, "functions", 25)

        result = adapt_plan(before, after)
        new_plan = result["plan"]
        changes = result["changes"]

        # data_types should now have 'relearn' activity
        functions_item = next((t for t in new_plan["recommended_topics"] if t["topic"] == "functions"), None)
        self.assertIsNotNone(functions_item)
        self.assertEqual(functions_item["activity"], "relearn")
        self.assertTrue(any("Topic 'functions' activity changed" in c for c in changes))

    def test_case_4_prerequisite_unlocks_next_topic(self):
        """Case 4: Prerequisite becomes 'good' and unlocks dependent topic directly."""
        before = self._load_learner("learner_prereq_gap.json")
        # In learner_prereq_gap: conditions is null, loops is 33% (weak)
        self.assertIsNone(before["mastery"]["conditions"])

        # Student assesses conditions and scores 78% (good)
        after = simulate_quiz_result(before, "conditions", 78)

        result = adapt_plan(before, after)
        new_plan = result["plan"]
        changes = result["changes"]

        # Now conditions is at 'good', so loops is no longer blocked by an unmastered prereq
        # Loops should now be the very first recommended topic!
        self.assertEqual(new_plan["recommended_topics"][0]["topic"], "loops")
        self.assertEqual(new_plan["recommended_topics"][0]["activity"], "relearn")
        self.assertTrue(any("Prerequisite 'conditions' achieved" in c for c in changes))


if __name__ == "__main__":
    unittest.main()
