
"""Unit tests for the topic recommender engine.

Tests all 8 test learners and verifies recommendation ordering,
activities, estimated durations, reasons, prerequisite constraints,
and mastery thresholds.
"""

import json
from pathlib import Path
import unittest

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
    _validate_metadata,
)


class TestConfigAndMastery(unittest.TestCase):
    """Test mastery level calculations and activity mappings."""

    def test_null_is_not_assessed(self):
        self.assertEqual(get_mastery_level(None), LEVEL_NOT_ASSESSED)
        self.assertEqual(
            get_activity_for_level(LEVEL_NOT_ASSESSED),
            "assess first",
        )

    def test_mastery_thresholds(self):
        self.assertEqual(get_mastery_level(0), LEVEL_WEAK)
        self.assertEqual(get_mastery_level(33), LEVEL_WEAK)
        self.assertEqual(get_mastery_level(39.9), LEVEL_WEAK)

        self.assertEqual(get_mastery_level(40), LEVEL_DEVELOPING)
        self.assertEqual(get_mastery_level(55), LEVEL_DEVELOPING)
        self.assertEqual(get_mastery_level(59.9), LEVEL_DEVELOPING)

        self.assertEqual(get_mastery_level(60), LEVEL_GOOD)
        self.assertEqual(get_mastery_level(79.9), LEVEL_GOOD)

        self.assertEqual(get_mastery_level(80), LEVEL_STRONG)
        self.assertEqual(get_mastery_level(100), LEVEL_STRONG)

    def test_activity_mapping(self):
        self.assertEqual(get_activity_for_level(LEVEL_WEAK), "relearn")
        self.assertEqual(get_activity_for_level(LEVEL_DEVELOPING), "revise")
        self.assertEqual(get_activity_for_level(LEVEL_GOOD), "practice")
        self.assertEqual(get_activity_for_level(LEVEL_STRONG), "advance")
        self.assertEqual(
            get_activity_for_level(LEVEL_NOT_ASSESSED),
            "assess first",
        )


class TestTopicsMetadata(unittest.TestCase):
    """Test loading and validation of topics.csv."""

    def test_topics_csv_structure(self):
        topics = load_topics_metadata()

        expected_ids = [
            "variables",
            "conditions",
            "loops",
            "functions",
            "lists",
            "dictionaries",
        ]

        topic_ids = [topic["topic_id"] for topic in topics]

        self.assertEqual(len(topics), 6)
        self.assertEqual(topic_ids, expected_ids)

        loops_info = next(
            topic for topic in topics
            if topic["topic_id"] == "loops"
        )
        self.assertIn("conditions", loops_info["prerequisites"])

        dictionaries_info = next(
            topic for topic in topics
            if topic["topic_id"] == "dictionaries"
        )
        self.assertIn("lists", dictionaries_info["prerequisites"])

    def test_unknown_prerequisite_rejected(self):
        topics = [
            {
                "topic_id": "variables",
                "order": 1,
                "prerequisites": ["unknown"],
                "est_minutes": 20,
            }
        ]

        with self.assertRaisesRegex(ValueError, "Unknown prerequisite"):
            _validate_metadata(topics)

    def test_circular_prerequisites_rejected(self):
        topics = [
            {
                "topic_id": "variables",
                "order": 1,
                "prerequisites": ["loops"],
                "est_minutes": 20,
            },
            {
                "topic_id": "loops",
                "order": 2,
                "prerequisites": ["variables"],
                "est_minutes": 20,
            },
        ]

        with self.assertRaisesRegex(ValueError, "Circular"):
            _validate_metadata(topics)

    def test_self_prerequisite_rejected(self):
        topics = [
            {
                "topic_id": "variables",
                "order": 1,
                "prerequisites": ["variables"],
                "est_minutes": 20,
            }
        ]

        with self.assertRaisesRegex(ValueError, "own prerequisite"):
            _validate_metadata(topics)


class TestEightLearners(unittest.TestCase):
    """Test recommendations for all 8 learner scenarios."""

    @classmethod
    def setUpClass(cls):
        cls.learners_dir = Path(__file__).resolve().parent / "test_learners"

    def _load_learner(self, filename: str) -> dict:
        filepath = self.learners_dir / filename

        with open(filepath, mode="r", encoding="utf-8") as file:
            return json.load(file)

    @staticmethod
    def _activity_map(recommendations):
        return {
            item["topic_id"]: item["activity"]
            for item in recommendations
        }

    @staticmethod
    def _topic_order(recommendations):
        return [
            item["topic_id"]
            for item in recommendations
        ]

    def test_recommendation_structure(self):
        data = self._load_learner("learner_all_weak.json")
        recommendations = recommend_topics(data)

        self.assertTrue(recommendations)

        for item in recommendations:
            self.assertEqual(
                set(item.keys()),
                {
                    "topic_id",
                    "activity",
                    "estimated_minutes",
                    "reason",
                },
            )
            self.assertIsInstance(item["topic_id"], str)
            self.assertIsInstance(item["activity"], str)
            self.assertIsInstance(item["estimated_minutes"], int)
            self.assertGreater(item["estimated_minutes"], 0)
            self.assertIsInstance(item["reason"], str)
            self.assertTrue(item["reason"])

    def test_learner_all_weak(self):
        """All weak topics should receive relearn recommendations."""

        data = self._load_learner("learner_all_weak.json")
        recommendations = recommend_topics(data)

        self.assertEqual(len(recommendations), 6)

        for item in recommendations:
            self.assertEqual(item["activity"], "relearn")

        order = self._topic_order(recommendations)

        self.assertLess(order.index("variables"), order.index("conditions"))
        self.assertLess(order.index("conditions"), order.index("loops"))
        self.assertLess(order.index("loops"), order.index("lists"))
        self.assertLess(order.index("lists"), order.index("dictionaries"))

    def test_learner_all_strong(self):
        """All strong topics should receive advance recommendations."""

        data = self._load_learner("learner_all_strong.json")
        recommendations = recommend_topics(data)

        self.assertEqual(len(recommendations), 6)

        for item in recommendations:
            self.assertEqual(item["activity"], "advance")

    def test_learner_mixed(self):
        """Verify recommendations for mixed mastery levels."""

        data = self._load_learner("learner_mixed.json")
        recommendations = recommend_topics(data)

        rec_dict = self._activity_map(recommendations)

        self.assertEqual(rec_dict["variables"], "advance")
        self.assertEqual(rec_dict["dictionaries"], "practice")
        self.assertEqual(rec_dict["conditions"], "revise")
        self.assertEqual(rec_dict["loops"], "relearn")
        self.assertEqual(rec_dict["functions"], "assess first")
        self.assertEqual(rec_dict["lists"], "assess first")

        order = self._topic_order(recommendations)

        self.assertLess(
            order.index("conditions"),
            order.index("loops"),
        )

    def test_learner_nothing_assessed(self):
        """All topics should be assessed in prerequisite order."""

        data = self._load_learner("learner_nothing_assessed.json")
        recommendations = recommend_topics(data)

        expected_topics = {
            "variables",
            "conditions",
            "loops",
            "functions",
            "lists",
            "dictionaries",
        }

        order = self._topic_order(recommendations)

        self.assertEqual(set(order), expected_topics)
        self.assertEqual(len(order), 6)

        self.assertLess(order.index("variables"), order.index("conditions"))
        self.assertLess(order.index("conditions"), order.index("loops"))
        self.assertLess(order.index("loops"), order.index("functions"))
        self.assertLess(order.index("loops"), order.index("lists"))
        self.assertLess(order.index("lists"), order.index("dictionaries"))

        for item in recommendations:
            self.assertEqual(item["activity"], "assess first")

    def test_learner_budget_30(self):
        """Verify activities for the 30-minute budget learner."""

        data = self._load_learner("learner_budget_30.json")
        recommendations = recommend_topics(data)

        rec_dict = self._activity_map(recommendations)

        self.assertEqual(rec_dict["conditions"], "relearn")
        self.assertEqual(rec_dict["dictionaries"], "practice")
        self.assertEqual(rec_dict["variables"], "advance")
        self.assertEqual(rec_dict["loops"], "assess first")

    def test_learner_budget_90(self):
        """Verify activities for the 90-minute budget learner."""

        data = self._load_learner("learner_budget_90.json")
        recommendations = recommend_topics(data)

        rec_dict = self._activity_map(recommendations)

        self.assertEqual(rec_dict["functions"], "relearn")
        self.assertEqual(rec_dict["loops"], "relearn")
        self.assertEqual(rec_dict["conditions"], "revise")

    def test_learner_one_weak(self):
        """A weak loops topic should be recommended first when prerequisites are mastered."""

        data = self._load_learner("learner_one_weak.json")
        recommendations = recommend_topics(data)

        self.assertEqual(recommendations[0]["topic_id"], "loops")
        self.assertEqual(recommendations[0]["activity"], "relearn")

        for item in recommendations[1:]:
            self.assertEqual(item["activity"], "advance")

    def test_learner_prereq_gap(self):
        """An unassessed prerequisite must be scheduled before a weak dependent topic."""

        data = self._load_learner("learner_prereq_gap.json")
        recommendations = recommend_topics(data)

        rec_dict = self._activity_map(recommendations)

        self.assertEqual(rec_dict["conditions"], "assess first")
        self.assertEqual(rec_dict["loops"], "relearn")

        order = self._topic_order(recommendations)

        self.assertLess(
            order.index("conditions"),
            order.index("loops"),
            "Conditions must be recommended before loops.",
        )


if __name__ == "__main__":
    unittest.main()
