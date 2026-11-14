
import unittest

from ai_engine.recommendation.adapter import normalize_analysis


class TestNormalizeAnalysis(unittest.TestCase):

    def test_actual_mastery_input(self):
        result = normalize_analysis({
            "learner_id": "student_01",
            "daily_minutes": 60,
            "mastery": {
                "variables": 85,
                "loops": 35,
                "functions": None
            }
        })

        self.assertEqual(result.learner_id, "student_01")
        self.assertEqual(result.daily_minutes, 60)
        self.assertEqual(result.topic_scores["variables"], 85.0)
        self.assertEqual(result.topic_scores["loops"], 35.0)
        self.assertIsNone(result.topic_scores["functions"])

    def test_alternative_daily_minutes(self):
        result = normalize_analysis({
            "daily_study_minutes": 30,
            "topics": {"loops": 50}
        })

        self.assertEqual(result.daily_minutes, 30)

    def test_dictionary_topic_objects(self):
        result = normalize_analysis({
            "topics": {
                "loops": {"score": 45},
                "functions": {"mastery_score": 75}
            }
        })

        self.assertEqual(result.topic_scores["loops"], 45.0)
        self.assertEqual(result.topic_scores["functions"], 75.0)

    def test_list_topic_format(self):
        result = normalize_analysis({
            "topics": [
                {"topic_id": "loops", "score": 40},
                {"topic": "functions", "mastery_score": 80}
            ]
        })

        self.assertEqual(result.topic_scores["loops"], 40.0)
        self.assertEqual(result.topic_scores["functions"], 80.0)

    def test_zero_daily_minutes_is_preserved(self):
        result = normalize_analysis({"daily_minutes": 0})
        self.assertEqual(result.daily_minutes, 0)

    def test_default_values(self):
        result = normalize_analysis({})
        self.assertEqual(result.learner_id, "anonymous_learner")
        self.assertEqual(result.daily_minutes, 60)

    def test_invalid_score_rejected(self):
        with self.assertRaises(ValueError):
            normalize_analysis({"mastery": {"loops": 110}})

    def test_negative_score_rejected(self):
        with self.assertRaises(ValueError):
            normalize_analysis({"mastery": {"loops": -5}})

    def test_boolean_score_rejected(self):
        with self.assertRaises(ValueError):
            normalize_analysis({"mastery": {"loops": True}})

    def test_invalid_daily_minutes_rejected(self):
        with self.assertRaises(ValueError):
            normalize_analysis({"daily_minutes": -10})

    def test_boolean_daily_minutes_rejected(self):
        with self.assertRaises(ValueError):
            normalize_analysis({"daily_minutes": True})

    def test_invalid_topic_id_rejected(self):
        with self.assertRaises(ValueError):
            normalize_analysis({"mastery": {"": 50}})


if __name__ == "__main__":
    unittest.main()
