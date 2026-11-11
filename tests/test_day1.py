import json
import unittest
from pathlib import Path

from ai_engine.common.schemas import TOPICS, mastery_level
from ai_engine.learner_analysis.profile import validate_profile

CONTRACTS = Path(__file__).resolve().parent.parent / "contracts"


def good_profile():
    return {
        "learner_id": "S101",
        "course": "python",
        "goal": "Learn Python programming",
        "level": "beginner",
        "daily_minutes": 60,
    }


class TestProfile(unittest.TestCase):
    def test_good_profile(self):
        self.assertEqual(validate_profile(good_profile()), [])

    def test_missing_course(self):
        p = good_profile()
        del p["course"]
        self.assertTrue(any("course" in e for e in validate_profile(p)))

    def test_wrong_level(self):
        p = good_profile()
        p["level"] = "expert"
        self.assertTrue(any("level" in e for e in validate_profile(p)))

    def test_negative_minutes(self):
        p = good_profile()
        p["daily_minutes"] = -5
        self.assertTrue(any("daily_minutes" in e for e in validate_profile(p)))

    def test_text_minutes(self):
        p = good_profile()
        p["daily_minutes"] = "60"
        self.assertTrue(any("daily_minutes" in e for e in validate_profile(p)))

    def test_empty_profile(self):
        errors = validate_profile({})
        self.assertEqual(len(errors), 5)

    def test_not_a_dict(self):
        self.assertEqual(validate_profile(None), ["profile must be a dictionary"])


class TestMastery(unittest.TestCase):
    def test_levels(self):
        self.assertEqual(mastery_level(0), "weak")
        self.assertEqual(mastery_level(39), "weak")
        self.assertEqual(mastery_level(40), "developing")
        self.assertEqual(mastery_level(59), "developing")
        self.assertEqual(mastery_level(60), "good")
        self.assertEqual(mastery_level(79), "good")
        self.assertEqual(mastery_level(80), "strong")
        self.assertEqual(mastery_level(100), "strong")

    def test_none_is_not_assessed(self):
        self.assertEqual(mastery_level(None), "not_assessed")

    def test_bad_scores(self):
        with self.assertRaises(ValueError):
            mastery_level(101)
        with self.assertRaises(ValueError):
            mastery_level(-1)
        with self.assertRaises(ValueError):
            mastery_level("80")


class TestSampleJson(unittest.TestCase):
    def test_samples_load_and_match_rules(self):
        profile = json.loads((CONTRACTS / "sample_profile.json").read_text())
        self.assertEqual(validate_profile(profile), [])

        analysis = json.loads((CONTRACTS / "sample_analysis.json").read_text())
        self.assertEqual(list(analysis["mastery"].keys()), TOPICS)
        for topic in analysis["not_assessed"]:
            self.assertIsNone(analysis["mastery"][topic])
        for topic in analysis["weak_topics"]:
            self.assertEqual(mastery_level(analysis["mastery"][topic]), "weak")

        quiz = json.loads((CONTRACTS / "sample_quiz_result.json").read_text())
        self.assertEqual(quiz["correct"] + len(quiz["wrong_question_ids"]), quiz["total"])

        plan = json.loads((CONTRACTS / "sample_plan.json").read_text())
        self.assertEqual(
            sum(item["minutes"] for item in plan["recommended_topics"]),
            plan["total_minutes"],
        )


if __name__ == "__main__":
    unittest.main()
