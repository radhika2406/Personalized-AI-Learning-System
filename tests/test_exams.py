"""
test_exams.py

Tests for the Three-Stage Examination System:
1. Stage 1 (Easy Examination) unlocks after 10 completed topics.
2. Stage 2 (Medium Examination) unlocks after next 5 topics (15 total) AND passing Stage 1.
3. Stage 3 (Hard Examination) unlocks after 16 topics AND passing Stage 2.
4. Skipping stages is strictly forbidden.
5. Generated exams contain only questions of the designated stage difficulty.
6. Attempt recording accurately captures questions, answers, score, difficulty, attempt, and status.
"""

import unittest

from assessment.scoring.exam_manager import (
    STAGE_1,
    STAGE_2,
    STAGE_3,
    is_stage_unlocked,
    generate_stage_exam,
    record_exam_attempt,
)
from assessment.question_bank.loader import load_course_topics, load_course_questions


class TestExamUnlockingAndProgression(unittest.TestCase):
    def setUp(self):
        self.course_id = "python"
        topics = load_course_topics(self.course_id)
        self.all_topic_ids = [t["id"] for t in topics]

    def test_stage_1_unlocking(self):
        """Stage 1 unlocks when at least 10 topics are completed."""
        # Under checkpoint (9 topics) -> Locked
        status_locked = is_stage_unlocked(self.course_id, STAGE_1, self.all_topic_ids[:9])
        self.assertFalse(status_locked["unlocked"])
        self.assertIn("Requires completing at least 10 topics", status_locked["reason"])

        # At checkpoint (10 topics) -> Unlocked
        status_unlocked = is_stage_unlocked(self.course_id, STAGE_1, self.all_topic_ids[:10])
        self.assertTrue(status_unlocked["unlocked"])

    def test_stage_2_requires_stage_1_completion_anti_skipping(self):
        """Stage 2 cannot be unlocked without passing Stage 1 even if 15 topics are completed."""
        completed_15 = self.all_topic_ids[:15]

        # 15 topics completed, but NO Stage 1 passed in exam history -> Locked
        status_skipped = is_stage_unlocked(self.course_id, STAGE_2, completed_15, exam_history=[])
        self.assertFalse(status_skipped["unlocked"])
        self.assertIn("Prerequisite Stage 1: Easy Examination must be passed", status_skipped["reason"])

        # Stage 1 was attempted but FAILED -> Locked
        failed_history = [{"stage": STAGE_1, "completion_status": "failed"}]
        status_failed = is_stage_unlocked(self.course_id, STAGE_2, completed_15, exam_history=failed_history)
        self.assertFalse(status_failed["unlocked"])

        # Stage 1 PASSED -> Unlocked
        passed_history = [{"stage": STAGE_1, "completion_status": "passed"}]
        status_ok = is_stage_unlocked(self.course_id, STAGE_2, completed_15, exam_history=passed_history)
        self.assertTrue(status_ok["unlocked"])

    def test_stage_3_requires_stage_2_completion_anti_skipping(self):
        """Stage 3 cannot be unlocked without passing Stage 2 even if all 16 topics are completed."""
        all_completed = self.all_topic_ids[:16]

        # Stage 1 passed, but Stage 2 not passed -> Locked
        history_only_stage1 = [{"stage": STAGE_1, "completion_status": "passed"}]
        status_stage3_locked = is_stage_unlocked(self.course_id, STAGE_3, all_completed, exam_history=history_only_stage1)
        self.assertFalse(status_stage3_locked["unlocked"])
        self.assertIn("Prerequisite Stage 2: Medium Examination must be passed", status_stage3_locked["reason"])

        # Both Stage 1 and Stage 2 passed -> Unlocked
        full_history = [
            {"stage": STAGE_1, "completion_status": "passed"},
            {"stage": STAGE_2, "completion_status": "passed"}
        ]
        status_stage3_ok = is_stage_unlocked(self.course_id, STAGE_3, all_completed, exam_history=full_history)
        self.assertTrue(status_stage3_ok["unlocked"])


class TestExamGenerationAndRecording(unittest.TestCase):
    def setUp(self):
        self.course_id = "python"
        topics = load_course_topics(self.course_id)
        self.all_topic_ids = [t["id"] for t in topics]
        self.questions = load_course_questions(self.course_id)

    def test_generate_exam_respects_difficulty(self):
        """Generated exams must contain questions matching the designated stage difficulty."""
        # Stage 1: Easy only
        exam1 = generate_stage_exam(self.course_id, STAGE_1, self.all_topic_ids[:10])
        self.assertEqual(exam1["difficulty"], "easy")
        self.assertTrue(len(exam1["questions"]) > 0)
        for q in exam1["questions"]:
            self.assertEqual(q["difficulty"].lower(), "easy")

        # Stage 2: Medium only
        history_s1 = [{"stage": STAGE_1, "completion_status": "passed"}]
        exam2 = generate_stage_exam(self.course_id, STAGE_2, self.all_topic_ids[:15], exam_history=history_s1)
        self.assertEqual(exam2["difficulty"], "medium")
        for q in exam2["questions"]:
            self.assertEqual(q["difficulty"].lower(), "medium")

        # Stage 3: Hard only
        history_s2 = [
            {"stage": STAGE_1, "completion_status": "passed"},
            {"stage": STAGE_2, "completion_status": "passed"}
        ]
        exam3 = generate_stage_exam(self.course_id, STAGE_3, self.all_topic_ids[:16], exam_history=history_s2)
        self.assertEqual(exam3["difficulty"], "hard")
        for q in exam3["questions"]:
            self.assertEqual(q["difficulty"].lower(), "hard")

    def test_cannot_generate_locked_exam(self):
        """Attempting to generate an exam when locked raises ValueError."""
        with self.assertRaises(ValueError):
            # Only 5 topics completed
            generate_stage_exam(self.course_id, STAGE_1, self.all_topic_ids[:5])

    def test_record_exam_attempt_passed(self):
        """Verify recording an exam attempt with a passing score."""
        sample_qids = list(self.questions.keys())[:5]
        sub_questions = {qid: self.questions[qid] for qid in sample_qids}
        perfect_answers = {qid: sub_questions[qid]["correct"] for qid in sample_qids}

        record = record_exam_attempt(
            learner_id="learner_001",
            course_id=self.course_id,
            stage=STAGE_1,
            answers=perfect_answers,
            questions=sub_questions,
            attempt_number=1,
            passing_score=60
        )

        self.assertEqual(record["learner_id"], "learner_001")
        self.assertEqual(record["course_id"], self.course_id)
        self.assertEqual(record["stage"], STAGE_1)
        self.assertEqual(record["difficulty"], "easy")
        self.assertEqual(record["attempt_number"], 1)
        self.assertEqual(record["score"], 100)
        self.assertEqual(record["completion_status"], "passed")
        self.assertEqual(record["correct_count"], 5)
        self.assertEqual(record["wrong_question_ids"], [])
        self.assertEqual(record["answers"], perfect_answers)

    def test_record_exam_attempt_failed(self):
        """Verify recording an exam attempt with a failing score."""
        sample_qids = list(self.questions.keys())[:5]
        sub_questions = {qid: self.questions[qid] for qid in sample_qids}
        # Choose wrong answers for all
        failing_answers = {
            qid: "a" if sub_questions[qid]["correct"] != "a" else "b"
            for qid in sample_qids
        }

        record = record_exam_attempt(
            learner_id="learner_002",
            course_id=self.course_id,
            stage=STAGE_1,
            answers=failing_answers,
            questions=sub_questions,
            attempt_number=1,
            passing_score=60
        )

        self.assertEqual(record["score"], 0)
        self.assertEqual(record["completion_status"], "failed")
        self.assertEqual(len(record["wrong_question_ids"]), 5)


if __name__ == "__main__":
    unittest.main()
