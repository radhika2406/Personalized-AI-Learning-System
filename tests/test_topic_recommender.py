"""Unit tests for the topic recommender engine.

Tests all 8 test learners and verifies ordering and activities,
specifically testing prerequisite constraints and mastery thresholds.
"""

import json
from pathlib import Path
import unittest

from ai_engine.recommendation.adapter import normalize_analysis
from ai_engine.recommendation.config import (
    LEVEL_WEAK,
    LEVEL_DEVELOPING,
    LEVEL_GOOD,
    LEVEL_STRONG,
    LEVEL_NOT_ASSESSED,
    get_mastery_level,
    get_activity_for_level,
)
from ai_engine.recommendation.topic_recommender import (
    load_topics_metadata,
    recommend_topics,
)


class TestConfigAndMastery(unittest.TestCase):
    """Test mastery level calculations and activity mappings."""

    def test_null_is_not_assessed(self):
        """None/null must always be 'not assessed', never treated as 0."""
        self.assertEqual(get_mastery_level(None), LEVEL_NOT_ASSESSED)
        self.assertEqual(get_activity_for_level(LEVEL_NOT_ASSESSED), "assess first")

    def test_mastery_thresholds(self):
        """Test threshold boundaries: weak < 40 <= developing < 60 <= good < 80 <= strong."""
        # Weak (< 40)
        self.assertEqual(get_mastery_level(0), LEVEL_WEAK)
        self.assertEqual(get_mastery_level(33), LEVEL_WEAK)
        self.assertEqual(get_mastery_level(39.9), LEVEL_WEAK)

        # Developing (40 to 69.9)
        self.assertEqual(get_mastery_level(40), LEVEL_DEVELOPING)
        self.assertEqual(get_mastery_level(55), LEVEL_DEVELOPING)
        self.assertEqual(get_mastery_level(59.9), LEVEL_DEVELOPING)

        # Good (60 to 79.9)
        self.assertEqual(get_mastery_level(60), LEVEL_GOOD)
        self.assertEqual(get_mastery_level(79.9), LEVEL_GOOD)

        # Strong (>= 80)
        self.assertEqual(get_mastery_level(80), LEVEL_STRONG)
        self.assertEqual(get_mastery_level(100), LEVEL_STRONG)

    def test_activity_mapping(self):
        """Test designated activity for each mastery level."""
        self.assertEqual(get_activity_for_level(LEVEL_WEAK), "relearn")
        self.assertEqual(get_activity_for_level(LEVEL_DEVELOPING), "revise")
        self.assertEqual(get_activity_for_level(LEVEL_GOOD), "practice")
        self.assertEqual(get_activity_for_level(LEVEL_STRONG), "advance")
        self.assertEqual(get_activity_for_level(LEVEL_NOT_ASSESSED), "assess first")


class TestTopicsMetadata(unittest.TestCase):
    """Test loading and structure of topics.csv."""

    def test_topics_csv_structure(self):
        topics = load_topics_metadata()
        self.assertEqual(len(topics), 6)

        topic_ids = [t["topic_id"] for t in topics]
        expected_ids = ["variables", "data_types", "conditions", "loops", "functions", "lists"]
        self.assertEqual(topic_ids, expected_ids)

        # Check prerequisite for loops contains conditions
        loops_info = next(t for t in topics if t["topic_id"] == "loops")
        self.assertIn("conditions", loops_info["prerequisites"])


class TestEightLearners(unittest.TestCase):
    """Test recommend_topics on all 8 test learners from tests/test_learners/."""

    @classmethod
    def setUpClass(cls):
        cls.learners_dir = Path(__file__).resolve().parent / "test_learners"

    def _load_learner(self, filename: str) -> dict:
        filepath = self.learners_dir / filename
        with open(filepath, mode="r", encoding="utf-8") as f:
            return json.load(f)

    def test_learner_all_weak(self):
        """Learner 1: All weak topics should get 'relearn' and respect prerequisite order."""
        data = self._load_learner("learner_all_weak.json")
        recommendations = recommend_topics(data)

        self.assertEqual(len(recommendations), 6)
        # All activities must be 'relearn'
        for _, activity in recommendations:
            self.assertEqual(activity, "relearn")

        # Variables must come before data_types, data_types before conditions, conditions before loops
        order = [tid for tid, _ in recommendations]
        self.assertLess(order.index("variables"), order.index("data_types"))
        self.assertLess(order.index("data_types"), order.index("conditions"))
        self.assertLess(order.index("conditions"), order.index("loops"))

    def test_learner_all_strong(self):
        """Learner 2: All strong topics should get 'advance'."""
        data = self._load_learner("learner_all_strong.json")
        recommendations = recommend_topics(data)

        self.assertEqual(len(recommendations), 6)
        for _, activity in recommendations:
            self.assertEqual(activity, "advance")

    def test_learner_mixed(self):
        """Learner 3: Mixed masteries."""
        data = self._load_learner("learner_mixed.json")
        recommendations = recommend_topics(data)
        rec_dict = dict(recommendations)

        self.assertEqual(rec_dict["variables"], "advance")
        self.assertEqual(rec_dict["data_types"], "practice")
        self.assertEqual(rec_dict["conditions"], "revise")
        self.assertEqual(rec_dict["loops"], "relearn")
        self.assertEqual(rec_dict["functions"], "assess first")
        self.assertEqual(rec_dict["lists"], "assess first")

        # Since conditions is at 'developing' (< 'good'), it must be recommended before loops
        order = [tid for tid, _ in recommendations]
        self.assertLess(order.index("conditions"), order.index("loops"))

    def test_learner_nothing_assessed(self):
        """Learner 4: Nothing assessed. All activities must be 'assess first' in curriculum order."""
        data = self._load_learner("learner_nothing_assessed.json")
        recommendations = recommend_topics(data)

        expected = [
            ("variables", "assess first"),
            ("data_types", "assess first"),
            ("conditions", "assess first"),
            ("loops", "assess first"),
            ("functions", "assess first"),
            ("lists", "assess first"),
        ]
        self.assertEqual(recommendations, expected)

    def test_learner_budget_30(self):
        """Learner 5: 30-minute budget learner."""
        data = self._load_learner("learner_budget_30.json")
        recommendations = recommend_topics(data)

        rec_dict = dict(recommendations)
        self.assertEqual(rec_dict["conditions"], "relearn")
        self.assertEqual(rec_dict["data_types"], "practice")
        self.assertEqual(rec_dict["variables"], "advance")
        self.assertEqual(rec_dict["loops"], "assess first")

    def test_learner_budget_90(self):
        """Learner 6: 90-minute budget learner."""
        data = self._load_learner("learner_budget_90.json")
        recommendations = recommend_topics(data)

        rec_dict = dict(recommendations)
        self.assertEqual(rec_dict["functions"], "relearn")
        self.assertEqual(rec_dict["loops"], "relearn")
        self.assertEqual(rec_dict["conditions"], "revise")

    def test_learner_one_weak(self):
        """Learner 7: Strong in everything except loops (weak).

        Because conditions is strong (already mastered), loops has its prerequisites
        satisfied and must be recommended first.
        """
        data = self._load_learner("learner_one_weak.json")
        recommendations = recommend_topics(data)

        # Loops must be first because it is weak and its prerequisites are satisfied
        self.assertEqual(recommendations[0], ("loops", "relearn"))

        # All other topics must be advance
        for tid, activity in recommendations[1:]:
            self.assertEqual(activity, "advance")

    def test_learner_prereq_gap(self):
        """Learner 8: Prerequisite problem (weak in loops but conditions not assessed).

        Conditions is not at 'good' or above, so conditions MUST be recommended
        before loops, even though loops is weak.
        """
        data = self._load_learner("learner_prereq_gap.json")
        recommendations = recommend_topics(data)
        rec_dict = dict(recommendations)

        self.assertEqual(rec_dict["conditions"], "assess first")
        self.assertEqual(rec_dict["loops"], "relearn")

        order = [tid for tid, _ in recommendations]
        # conditions must come before loops
        self.assertLess(
            order.index("conditions"),
            order.index("loops"),
            "Expected conditions to be recommended before loops when conditions is not assessed",
        )


if __name__ == "__main__":
    unittest.main()
