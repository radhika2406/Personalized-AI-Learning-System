import unittest

from assessment.scoring.score_quiz import load_questions, score_quiz
from ai_engine.common.schemas import TOPICS

QUESTIONS = load_questions()


def answers_for(topic, wrong_ids=()):
    """Build a full answer sheet for a topic: right answers, except wrong_ids."""
    sheet = {}
    for qid, row in QUESTIONS.items():
        if row["topic_id"] != topic:
            continue
        right = row["correct"]
        if qid in wrong_ids:
            right = "a" if right != "a" else "b"
        sheet[qid] = right
    return sheet


class TestQuestionBank(unittest.TestCase):
    def test_counts(self):
        self.assertEqual(len(QUESTIONS), 36)
        for topic in TOPICS:
            rows = [r for r in QUESTIONS.values() if r["topic_id"] == topic]
            self.assertEqual(len(rows), 6, topic)
            levels = sorted(r["difficulty"] for r in rows)
            self.assertEqual(levels, ["easy"] * 3 + ["hard"] + ["medium"] * 2, topic)

    def test_rows_are_clean(self):
        for qid, r in QUESTIONS.items():
            self.assertIn(r["topic_id"], TOPICS)
            self.assertTrue(qid.startswith(r["topic_id"] + "_q"))
            self.assertIn(r["correct"], ["a", "b", "c", "d"])
            for col in ["question", "option_a", "option_b", "option_c", "option_d", "explanation"]:
                self.assertTrue(r[col].strip(), f"{qid} has empty {col}")


class TestScoreQuiz(unittest.TestCase):
    def test_all_right(self):
        r = score_quiz("S1", "loops", answers_for("loops"), QUESTIONS)
        self.assertEqual(r["score_pct"], 100)
        self.assertEqual(r["correct"], 6)
        self.assertEqual(r["wrong_question_ids"], [])

    def test_all_wrong(self):
        wrong = [q for q, r in QUESTIONS.items() if r["topic_id"] == "loops"]
        r = score_quiz("S1", "loops", answers_for("loops", wrong), QUESTIONS)
        self.assertEqual(r["score_pct"], 0)
        self.assertEqual(len(r["wrong_question_ids"]), 6)

    def test_some_wrong_matches_contract(self):
        r = score_quiz("S1", "loops", answers_for("loops", ["loops_q3", "loops_q5"]), QUESTIONS, attempt=2)
        self.assertEqual(r["score_pct"], 67)
        self.assertEqual(r["wrong_question_ids"], ["loops_q3", "loops_q5"])
        self.assertEqual(r["attempt"], 2)
        self.assertEqual(
            set(r),
            {"learner_id", "course", "topic", "score_pct", "correct", "total", "attempt", "wrong_question_ids"},
        )

    def test_empty_answers(self):
        with self.assertRaises(ValueError):
            score_quiz("S1", "loops", {}, QUESTIONS)

    def test_unknown_question(self):
        with self.assertRaises(ValueError):
            score_quiz("S1", "loops", {"loops_q99": "a"}, QUESTIONS)

    def test_question_from_other_topic(self):
        with self.assertRaises(ValueError):
            score_quiz("S1", "loops", {"variables_q1": "c"}, QUESTIONS)

    def test_unknown_topic(self):
        with self.assertRaises(ValueError):
            score_quiz("S1", "recursion", {"loops_q1": "b"}, QUESTIONS)

    def test_skipped_counts_as_wrong(self):
        r = score_quiz("S1", "loops", {"loops_q1": "b", "loops_q2": ""}, QUESTIONS)
        self.assertEqual(r["correct"], 1)
        self.assertEqual(r["wrong_question_ids"], ["loops_q2"])

    def test_bad_letter(self):
        with self.assertRaises(ValueError):
            score_quiz("S1", "loops", {"loops_q1": "z"}, QUESTIONS)

    def test_capital_letter_ok(self):
        r = score_quiz("S1", "loops", {"loops_q1": " B "}, QUESTIONS)
        self.assertEqual(r["score_pct"], 100)


if __name__ == "__main__":
    unittest.main()
