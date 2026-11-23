import sys
from pathlib import Path
import unittest
from types import SimpleNamespace
from unittest.mock import patch

# Make the backend package available during test discovery.
BACKEND_PATH = Path(__file__).resolve().parents[1] / "backend"
sys.path.insert(0, str(BACKEND_PATH))

from app.services import quiz_attempt_service


class FakeQuery:
    def __init__(self, records):
        self.records = records

    def filter(self, *args, **kwargs):
        return self

    def all(self):
        return self.records


class FakeDB:
    def __init__(self, answers, questions):
        self.answers = answers
        self.questions = questions
        self.query_count = 0

    def query(self, model):
        self.query_count += 1

        if self.query_count == 1:
            return FakeQuery(self.answers)

        if self.query_count == 2:
            return FakeQuery(self.questions)

        raise AssertionError("Unexpected database query")


class TestQuizAttemptReview(unittest.TestCase):

    def setUp(self):
        self.question = SimpleNamespace(
            id=1,
            question_text="What is the output of 2 + 2?",
            option_a="4",
            option_b="5",
            option_c="6",
            option_d="8",
            correct_option="A",
            explanation="Adding 2 and 2 gives 4.",
        )

        self.answer = SimpleNamespace(
            question_id=1,
            selected_option="B",
        )

        self.attempt = SimpleNamespace(
            id=10,
            quiz_id=20,
        )

        self.db = FakeDB(
            answers=[self.answer],
            questions=[self.question],
        )

    @patch(
        "app.services.quiz_attempt_service.explain_wrong_answer"
    )
    def test_wrong_answer_uses_ai_explanation(self, mock_explainer):
        mock_explainer.return_value = "AI-generated explanation."

        review = quiz_attempt_service.build_attempt_review(
            self.db,
            self.attempt,
            include_ai_explanations=True,
        )

        mock_explainer.assert_called_once_with(
            question="What is the output of 2 + 2?",
            chosen_answer="5",
            correct_answer="4",
            explanation="Adding 2 and 2 gives 4.",
        )

        self.assertEqual(
            review[0]["explanation"],
            "AI-generated explanation.",
        )
        self.assertFalse(review[0]["is_correct"])

    @patch(
        "app.services.quiz_attempt_service.explain_wrong_answer"
    )
    def test_correct_answer_does_not_call_ai(self, mock_explainer):
        self.answer.selected_option = "A"

        review = quiz_attempt_service.build_attempt_review(
            self.db,
            self.attempt,
            include_ai_explanations=True,
        )

        mock_explainer.assert_not_called()

        self.assertEqual(
            review[0]["explanation"],
            "Adding 2 and 2 gives 4.",
        )
        self.assertTrue(review[0]["is_correct"])

    @patch(
        "app.services.quiz_attempt_service.explain_wrong_answer"
    )
    def test_ai_failure_uses_original_explanation(self, mock_explainer):
        mock_explainer.side_effect = RuntimeError("Gemini unavailable")

        review = quiz_attempt_service.build_attempt_review(
            self.db,
            self.attempt,
            include_ai_explanations=True,
        )

        self.assertEqual(
            review[0]["explanation"],
            "Adding 2 and 2 gives 4.",
        )

    @patch(
        "app.services.quiz_attempt_service.explain_wrong_answer"
    )
    def test_ai_is_not_called_by_default(self, mock_explainer):
        review = quiz_attempt_service.build_attempt_review(
            self.db,
            self.attempt,
        )

        mock_explainer.assert_not_called()

        self.assertEqual(
            review[0]["explanation"],
            "Adding 2 and 2 gives 4.",
        )

    @patch.object(quiz_attempt_service, "build_attempt_review")
    @patch.object(quiz_attempt_service, "get_attempt_by_id")
    def test_detailed_review_enables_ai(
        self,
        mock_get_attempt,
        mock_build_review,
    ):
        mock_get_attempt.return_value = self.attempt
        mock_build_review.return_value = []

        quiz_attempt_service.get_attempt_review(
            self.db,
            attempt_id=10,
            user_id=5,
        )

        mock_build_review.assert_called_once_with(
            self.db,
            self.attempt,
            include_ai_explanations=True,
        )


if __name__ == "__main__":
    unittest.main()
