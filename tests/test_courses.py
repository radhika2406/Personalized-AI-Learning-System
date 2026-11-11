"""
test_courses.py

Tests to verify:
1. All 3 categories exist and have their assigned courses.
2. All 12 courses exist with complete directory structures.
3. Every course has a valid syllabus.json and topics.json with 16 topics.
4. Every topic has questions at all three difficulty levels (Easy, Medium, Hard).
5. Course loader utilities operate cleanly across all courses.
"""

import unittest
from pathlib import Path

from ai_engine.common.course_config import (
    CATEGORIES,
    COURSES,
    list_categories,
    list_courses,
    get_course,
    get_category,
    get_courses_by_category,
    get_course_checkpoints,
)
from assessment.question_bank.loader import (
    load_course_syllabus,
    load_course_topics,
    load_course_questions,
    get_questions_by_topic,
    get_questions_by_difficulty,
)


class TestCourseStructureAndConfiguration(unittest.TestCase):
    def test_three_categories_exist(self):
        """Verify all three required categories exist."""
        expected_cats = {"programming", "ai_ml_data_science", "computer_science"}
        self.assertEqual(set(list_categories()), expected_cats)
        for cat_id in expected_cats:
            cat = get_category(cat_id)
            self.assertIsNotNone(cat)
            self.assertTrue(len(cat["course_ids"]) >= 4)

    def test_all_twelve_courses_exist(self):
        """Verify all 12 courses exist in configuration."""
        expected_courses = {
            # Category A
            "python", "java", "cpp", "dsa",
            # Category B
            "machine_learning", "deep_learning", "data_science", "neural_networks",
            # Category C
            "dbms", "operating_systems", "computer_networks", "oop"
        }
        self.assertEqual(set(list_courses()), expected_courses)
        self.assertEqual(len(COURSES), 12)

    def test_courses_grouped_correctly(self):
        """Verify courses are correctly mapped to their categories."""
        prog = [c["id"] for c in get_courses_by_category("programming")]
        self.assertEqual(sorted(prog), ["cpp", "dsa", "java", "python"])

        aiml = [c["id"] for c in get_courses_by_category("ai_ml_data_science")]
        self.assertEqual(sorted(aiml), ["data_science", "deep_learning", "machine_learning", "neural_networks"])

        cs = [c["id"] for c in get_courses_by_category("computer_science")]
        self.assertEqual(sorted(cs), ["computer_networks", "dbms", "oop", "operating_systems"])

    def test_course_files_exist_on_disk(self):
        """Verify that syllabus, topics, and questions files exist for every course."""
        for course_id, info in COURSES.items():
            course_dir = Path(info["path"])
            self.assertTrue(course_dir.is_dir(), f"Directory missing for {course_id}: {course_dir}")
            self.assertTrue((course_dir / "syllabus.json").is_file(), f"syllabus.json missing for {course_id}")
            self.assertTrue((course_dir / "topics.json").is_file(), f"topics.json missing for {course_id}")
            self.assertTrue((course_dir / "questions.csv").is_file(), f"questions.csv missing for {course_id}")


class TestCourseContentAndSyllabus(unittest.TestCase):
    def test_every_course_has_sixteen_topics(self):
        """Verify every course contains exactly 16 logically ordered topics."""
        for course_id in list_courses():
            topics = load_course_topics(course_id)
            self.assertEqual(len(topics), 16, f"Course {course_id} should have 16 topics, found {len(topics)}")

            orders = [t["order"] for t in topics]
            self.assertEqual(orders, list(range(1, 17)), f"Topics in {course_id} must be sequentially ordered 1..16")

            stages = [t.get("difficulty_stage") for t in topics]
            # First 10 beginner, next 5 intermediate, 16th advanced
            self.assertEqual(stages[:10], ["beginner"] * 10, f"First 10 topics of {course_id} must be beginner")
            self.assertEqual(stages[10:15], ["intermediate"] * 5, f"Topics 11-15 of {course_id} must be intermediate")
            self.assertEqual(stages[15:], ["advanced"], f"Topic 16 of {course_id} must be advanced")

    def test_syllabus_matches_topics_and_checkpoints(self):
        """Verify syllabus.json contains checkpoints matching the 3 examination stages."""
        for course_id in list_courses():
            syllabus = load_course_syllabus(course_id)
            self.assertIn("checkpoints", syllabus, f"checkpoints missing in {course_id}")
            checkpoints = syllabus["checkpoints"]
            self.assertEqual(checkpoints["stage_1_easy_exam"], 10)
            self.assertEqual(checkpoints["stage_2_medium_exam"], 15)
            self.assertEqual(checkpoints["stage_3_hard_exam"], 16)

            # Topics in syllabus match topics.json
            self.assertEqual(len(syllabus["topics"]), 16)

    def test_topic_question_distribution(self):
        """Verify each course has 96 questions: exactly 3 Easy, 2 Medium, 1 Hard per topic."""
        for course_id in list_courses():
            topics = load_course_topics(course_id)
            questions = load_course_questions(course_id)
            self.assertEqual(len(questions), 96, f"{course_id} must have 96 questions")

            easy_all = get_questions_by_difficulty(course_id, "easy")
            med_all = get_questions_by_difficulty(course_id, "medium")
            hard_all = get_questions_by_difficulty(course_id, "hard")
            self.assertEqual(len(easy_all), 48, f"{course_id} must have 48 easy questions")
            self.assertEqual(len(med_all), 32, f"{course_id} must have 32 medium questions")
            self.assertEqual(len(hard_all), 16, f"{course_id} must have 16 hard questions")

            # Check per-topic questions
            for topic in topics:
                tid = topic["id"]
                tq = get_questions_by_topic(course_id, tid)
                self.assertEqual(len(tq), 6, f"{course_id} topic {tid} must have 6 questions")

                t_easy = [q for q in tq if q["difficulty"].lower() == "easy"]
                t_med = [q for q in tq if q["difficulty"].lower() == "medium"]
                t_hard = [q for q in tq if q["difficulty"].lower() == "hard"]
                self.assertEqual(len(t_easy), 3, f"{course_id} {tid} must have 3 easy questions")
                self.assertEqual(len(t_med), 2, f"{course_id} {tid} must have 2 medium questions")
                self.assertEqual(len(t_hard), 1, f"{course_id} {tid} must have 1 hard question")


if __name__ == "__main__":
    unittest.main()
