"""
test_validation.py

Tests to verify:
1. All 1,152 question IDs are globally unique across all 12 courses.
2. All questions contain valid answer keys ('a', 'b', 'c', 'd').
3. All questions have non-empty text, four non-empty options, and non-empty explanations.
4. Difficulty labels strictly conform to Easy, Medium, or Hard.
5. Validator properly catches corrupt data (missing fields, duplicate IDs, invalid choices).
"""

import unittest

from assessment.question_management.loader import load_all_questions
from assessment.question_management.validator import (
    validate_course,
    validate_all_courses,
    validate_question,
    VALID_DIFFICULTIES,
    VALID_ANSWER_KEYS,
)
from ai_engine.common.course_config import list_courses


class TestQuestionBankValidation(unittest.TestCase):
    def test_all_twelve_courses_pass_validation(self):
        """Validate all courses individually and check aggregated results."""
        is_valid, errors, summary = validate_all_courses()
        self.assertTrue(is_valid, f"Validation failed with errors: {errors[:5]}")
        self.assertEqual(len(errors), 0)
        self.assertEqual(summary["total_courses"], 12)
        self.assertEqual(summary["valid_courses"], 12)
        self.assertEqual(summary["total_questions"], 1152)
        self.assertEqual(summary["easy_count"], 576)
        self.assertEqual(summary["medium_count"], 384)
        self.assertEqual(summary["hard_count"], 192)

    def test_global_question_id_uniqueness(self):
        """Ensure no duplicate question ID exists across all 12 courses."""
        all_q = load_all_questions()
        self.assertEqual(len(all_q), 1152)
        unique_ids = set(all_q.keys())
        self.assertEqual(len(unique_ids), 1152)

    def test_question_fields_and_answer_integrity(self):
        """Ensure every question has clean, non-empty options, valid answer key, and valid difficulty."""
        all_q = load_all_questions()
        for qid, q in all_q.items():
            self.assertIn(
                q.get("difficulty", "").lower(),
                VALID_DIFFICULTIES,
                f"{qid} has invalid difficulty"
            )
            self.assertIn(
                q.get("correct", "").lower(),
                VALID_ANSWER_KEYS,
                f"{qid} has invalid correct key"
            )
            for opt in ["option_a", "option_b", "option_c", "option_d"]:
                val = str(q.get(opt, "")).strip()
                self.assertTrue(val, f"{qid} has empty option {opt}")
            self.assertTrue(str(q.get("question", "")).strip(), f"{qid} has empty question text")
            self.assertTrue(str(q.get("explanation", "")).strip(), f"{qid} has empty explanation")


class TestValidatorErrorDetection(unittest.TestCase):
    def test_catches_invalid_difficulty(self):
        bad_q = {
            "question_id": "test_q1", "category": "programming", "course": "python",
            "topic": "variables", "difficulty": "super_hard", "question": "What is x?",
            "option_a": "1", "option_b": "2", "option_c": "3", "option_d": "4",
            "correct": "a", "explanation": "x is 1"
        }
        errs = validate_question(bad_q)
        self.assertTrue(any("invalid difficulty" in e for e in errs))

    def test_catches_invalid_correct_key(self):
        bad_q = {
            "question_id": "test_q2", "category": "programming", "course": "python",
            "topic": "variables", "difficulty": "easy", "question": "What is x?",
            "option_a": "1", "option_b": "2", "option_c": "3", "option_d": "4",
            "correct": "e", "explanation": "x is 1"
        }
        errs = validate_question(bad_q)
        self.assertTrue(any("invalid correct key" in e for e in errs))

    def test_catches_empty_option(self):
        bad_q = {
            "question_id": "test_q3", "category": "programming", "course": "python",
            "topic": "variables", "difficulty": "easy", "question": "What is x?",
            "option_a": "1", "option_b": "", "option_c": "3", "option_d": "4",
            "correct": "a", "explanation": "x is 1"
        }
        errs = validate_question(bad_q)
        self.assertTrue(any("empty" in e for e in errs))

    def test_catches_missing_id(self):
        bad_q = {
            "question_id": "", "category": "programming", "course": "python",
            "topic": "variables", "difficulty": "easy", "question": "What is x?",
            "option_a": "1", "option_b": "2", "option_c": "3", "option_d": "4",
            "correct": "a", "explanation": "x is 1"
        }
        errs = validate_question(bad_q)
        self.assertTrue(any("missing question_id" in e for e in errs))


if __name__ == "__main__":
    unittest.main()
