'''
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
'''

import unittest

from assessment.scoring.score_quiz import load_questions, score_quiz
from assessment.question_management.loader import load_course_topics
from ai_engine.common.course_config import list_courses


COURSE_IDS = list_courses()


def get_topic_id(topic):
    """Support both normalized topic ID field names."""
    return topic.get("id") or topic.get("topic_id")


def answers_for(questions, topic_id, wrong_ids=()):
    """
    Build an answer sheet for a topic.
    All answers are correct except the selected wrong question IDs.
    """
    sheet = {}

    for question_id, row in questions.items():
        question_topic = row.get("topic_id") or row.get("topic")

        if question_topic != topic_id:
            continue

        right_answer = row["correct"]

        if question_id in wrong_ids:
            right_answer = "a" if right_answer != "a" else "b"

        sheet[question_id] = right_answer

    return sheet


class TestQuestionBank(unittest.TestCase):

    def test_all_twelve_courses_have_questions(self):
        """Every registered course must have a question bank."""

        self.assertEqual(len(COURSE_IDS), 12)

        for course_id in COURSE_IDS:
            with self.subTest(course=course_id):
                questions = load_questions(course_id)

                self.assertTrue(
                    questions,
                    f"No questions found for {course_id}"
                )

    def test_every_topic_has_six_questions(self):
        """Every topic should have its expected six questions."""

        for course_id in COURSE_IDS:
            with self.subTest(course=course_id):

                questions = load_questions(course_id)
                topics = load_course_topics(course_id)

                for topic in topics:
                    topic_id = get_topic_id(topic)

                    topic_questions = [
                        row
                        for row in questions.values()
                        if (row.get("topic_id") or row.get("topic"))
                        == topic_id
                    ]

                    self.assertEqual(
                        len(topic_questions),
                        6,
                        f"{course_id}: incorrect question count for {topic_id}"
                    )

    def test_difficulty_distribution_for_all_courses(self):
        """Every topic should have 3 easy, 2 medium and 1 hard question."""

        expected_distribution = (
            ["easy"] * 3
            + ["hard"]
            + ["medium"] * 2
        )

        for course_id in COURSE_IDS:
            with self.subTest(course=course_id):

                questions = load_questions(course_id)
                topics = load_course_topics(course_id)

                for topic in topics:
                    topic_id = get_topic_id(topic)

                    topic_questions = [
                        row
                        for row in questions.values()
                        if (row.get("topic_id") or row.get("topic"))
                        == topic_id
                    ]

                    actual_distribution = sorted(
                        row["difficulty"].strip().lower()
                        for row in topic_questions
                    )

                    self.assertEqual(
                        actual_distribution,
                        expected_distribution,
                        f"{course_id}: difficulty distribution incorrect "
                        f"for {topic_id}"
                    )

    def test_rows_are_clean_for_all_courses(self):
        """Validate the basic structure of every question."""

        required_fields = [
            "question_id",
            "topic_id",
            "correct",
            "difficulty",
            "question",
            "option_a",
            "option_b",
            "option_c",
            "option_d",
            "explanation",
        ]

        for course_id in COURSE_IDS:
            with self.subTest(course=course_id):

                questions = load_questions(course_id)
                topics = load_course_topics(course_id)

                valid_topic_ids = {
                    get_topic_id(topic)
                    for topic in topics
                }

                for question_id, row in questions.items():

                    for field in required_fields:
                        self.assertTrue(
                            str(row.get(field, "")).strip(),
                            f"{course_id}: {question_id} has empty {field}"
                        )

                    topic_id = row.get("topic_id") or row.get("topic")

                    self.assertIn(
                        topic_id,
                        valid_topic_ids,
                        f"{course_id}: unknown topic in {question_id}"
                    )

                    self.assertEqual(
                        question_id,
                        row["question_id"]
                    )

                    self.assertIn(
                        row["correct"].strip().lower(),
                        ["a", "b", "c", "d"]
                    )

                    self.assertIn(
                        row["difficulty"].strip().lower(),
                        ["easy", "medium", "hard"]
                    )


class TestScoreQuiz(unittest.TestCase):

    def test_all_right(self):
        """All correct answers should produce 100 percent."""

        questions = load_questions("python")
        topic_id = "loops"

        answers = answers_for(questions, topic_id)

        result = score_quiz(
            "S1",
            topic_id,
            answers,
            questions,
            course_id="python"
        )

        self.assertEqual(result["score_pct"], 100)
        self.assertEqual(result["correct"], len(answers))
        self.assertEqual(result["wrong_question_ids"], [])

    def test_all_wrong(self):
        """All incorrect answers should produce zero percent."""

        questions = load_questions("python")
        topic_id = "loops"

        wrong_ids = [
            question_id
            for question_id, row in questions.items()
            if (row.get("topic_id") or row.get("topic")) == topic_id
        ]

        answers = answers_for(
            questions,
            topic_id,
            wrong_ids
        )

        result = score_quiz(
            "S1",
            topic_id,
            answers,
            questions,
            course_id="python"
        )

        self.assertEqual(result["score_pct"], 0)
        self.assertEqual(
            len(result["wrong_question_ids"]),
            len(answers)
        )

    def test_some_wrong_matches_contract(self):
        """The result must follow Contract 1."""

        questions = load_questions("python")
        topic_id = "loops"

        topic_question_ids = [
            question_id
            for question_id, row in questions.items()
            if (row.get("topic_id") or row.get("topic")) == topic_id
        ]

        wrong_ids = topic_question_ids[:2]

        answers = answers_for(
            questions,
            topic_id,
            wrong_ids
        )

        result = score_quiz(
            "S1",
            topic_id,
            answers,
            questions,
            attempt=2,
            course_id="python"
        )

        expected_score = round(
            (len(answers) - len(wrong_ids)) / len(answers) * 100
        )

        self.assertEqual(result["score_pct"], expected_score)
        self.assertEqual(result["wrong_question_ids"], wrong_ids)
        self.assertEqual(result["attempt"], 2)

        self.assertEqual(
            set(result),
            {
                "learner_id",
                "course",
                "topic",
                "score_pct",
                "correct",
                "total",
                "attempt",
                "wrong_question_ids",
            }
        )

    def test_scoring_works_for_all_twelve_courses(self):
        """The same scoring function must work for every course."""

        for course_id in COURSE_IDS:
            with self.subTest(course=course_id):

                questions = load_questions(course_id)
                topics = load_course_topics(course_id)

                topic_id = get_topic_id(topics[0])

                answers = answers_for(
                    questions,
                    topic_id
                )

                result = score_quiz(
                    learner_id="S101",
                    topic=topic_id,
                    answers=answers,
                    questions=questions,
                    course_id=course_id
                )

                self.assertEqual(result["course"], course_id)
                self.assertEqual(result["topic"], topic_id)
                self.assertEqual(result["score_pct"], 100)
                self.assertEqual(result["correct"], len(answers))

    def test_empty_answers(self):
        questions = load_questions("python")

        with self.assertRaises(ValueError):
            score_quiz(
                "S1",
                "loops",
                {},
                questions,
                course_id="python"
            )

    def test_unknown_question(self):
        questions = load_questions("python")

        with self.assertRaises(ValueError):
            score_quiz(
                "S1",
                "loops",
                {"loops_q99": "a"},
                questions,
                course_id="python"
            )

    def test_question_from_other_topic(self):
        questions = load_questions("python")

        with self.assertRaises(ValueError):
            score_quiz(
                "S1",
                "loops",
                {"variables_q1": "c"},
                questions,
                course_id="python"
            )

    def test_unknown_topic(self):
        questions = load_questions("python")

        with self.assertRaises(ValueError):
            score_quiz(
                "S1",
                "recursion",
                {"loops_q1": "b"},
                questions,
                course_id="python"
            )

    def test_skipped_counts_as_wrong(self):
        questions = load_questions("python")

        result = score_quiz(
            "S1",
            "loops",
            {
                "loops_q1": "b",
                "loops_q2": ""
            },
            questions,
            course_id="python"
        )

        self.assertEqual(result["correct"], 1)
        self.assertEqual(result["wrong_question_ids"], ["loops_q2"])

    def test_bad_letter(self):
        questions = load_questions("python")

        with self.assertRaises(ValueError):
            score_quiz(
                "S1",
                "loops",
                {"loops_q1": "z"},
                questions,
                course_id="python"
            )

    def test_capital_letter_ok(self):
        questions = load_questions("python")

        result = score_quiz(
            "S1",
            "loops",
            {"loops_q1": " B "},
            questions,
            course_id="python"
        )

        self.assertEqual(result["score_pct"], 100)


if __name__ == "__main__":
    unittest.main()
