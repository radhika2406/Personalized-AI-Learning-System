import argparse
import csv
import json
import sys
from pathlib import Path

from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.models.category import Category
from app.models.course import Course
from app.models.topic import Topic
from app.models.quiz import Quiz
from app.models.question import Question


# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------

ROOT = Path(__file__).resolve().parents[1] / "courses"

CATEGORY_NAMES = {
    "ai_ml_data_science": "AI, ML & Data Science",
    "computer_science": "Computer Science",
    "programming": "Programming",
}

EXPECTED_COURSES = 12
EXPECTED_TOPICS_PER_COURSE = 16
EXPECTED_QUESTIONS_PER_COURSE = 96

TOTALS = {
    "courses": 0,
    "topics": 0,
    "quizzes": 0,
    "questions": 0,
}


# --------------------------------------------------
# SOURCE FILE HELPERS
# --------------------------------------------------

def read_json(path: Path):
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def read_questions(path: Path):
    with path.open(
        "r",
        encoding="utf-8-sig",
        newline=""
    ) as file:
        return list(csv.DictReader(file))


def normalize_topic(raw_topic: dict):
    return {
        "source_topic_id": str(
            raw_topic.get("topic_id") or raw_topic.get("id")
        ),
        "title": (
            raw_topic.get("title")
            or raw_topic.get("name")
        ),
        "description": raw_topic.get("description"),
        "sequence_number": int(raw_topic.get("order", 1)),
        "difficulty_level": (
            raw_topic.get("difficulty_level")
            or raw_topic.get("level")
            or raw_topic.get("difficulty_stage")
        ),
        "subtopics": raw_topic.get("subtopics"),
        "prerequisites": raw_topic.get("prerequisites"),
    }


def load_course(folder: Path):
    syllabus_path = folder / "syllabus.json"
    topics_path = folder / "topics.json"
    questions_path = folder / "questions.csv"

    for path in (syllabus_path, topics_path, questions_path):
        if not path.is_file():
            raise ValueError(f"Missing source file: {path}")

    syllabus = read_json(syllabus_path)
    raw_topics = read_json(topics_path)
    questions = read_questions(questions_path)

    course_code = syllabus.get("course_id")
    course_title = (
        syllabus.get("course_title")
        or syllabus.get("course_name")
    )

    category_code = folder.parent.name

    if not course_code or not course_title:
        raise ValueError(
            f"Missing course ID or title in {syllabus_path}"
        )

    if len(course_code) > 20:
        raise ValueError(
            f"Course code exceeds 20 characters: {course_code}"
        )

    if category_code not in CATEGORY_NAMES:
        raise ValueError(
            f"Unknown category folder: {category_code}"
        )

    if not isinstance(raw_topics, list):
        raise ValueError(
            f"topics.json must contain a list: {topics_path}"
        )

    if len(raw_topics) != EXPECTED_TOPICS_PER_COURSE:
        raise ValueError(
            f"{course_code}: expected "
            f"{EXPECTED_TOPICS_PER_COURSE} topics, "
            f"found {len(raw_topics)}"
        )

    if len(questions) != EXPECTED_QUESTIONS_PER_COURSE:
        raise ValueError(
            f"{course_code}: expected "
            f"{EXPECTED_QUESTIONS_PER_COURSE} questions, "
            f"found {len(questions)}"
        )

    topics = [normalize_topic(item) for item in raw_topics]

    topic_ids = {
        topic["source_topic_id"] for topic in topics
    }

    if None in topic_ids or "None" in topic_ids:
        raise ValueError(
            f"{course_code}: a topic has no source ID"
        )

    if len(topic_ids) != len(topics):
        raise ValueError(
            f"{course_code}: duplicate topic IDs found"
        )

    for topic in topics:
        if not topic["title"]:
            raise ValueError(
                f"{course_code}: topic title is missing"
            )

    question_ids = set()

    for row in questions:
        required_fields = [
            "question_id",
            "topic",
            "difficulty",
            "question",
            "option_a",
            "option_b",
            "option_c",
            "option_d",
            "correct",
            "explanation",
        ]

        for field in required_fields:
            if not row.get(field):
                raise ValueError(
                    f"{course_code}: missing {field} "
                    f"in a question"
                )

        question_id = row["question_id"].strip()

        if question_id in question_ids:
            raise ValueError(
                f"{course_code}: duplicate question ID "
                f"{question_id}"
            )

        question_ids.add(question_id)

        if row["topic"].strip() not in topic_ids:
            raise ValueError(
                f"{course_code}: question {question_id} "
                f"references unknown topic {row['topic']}"
            )

        if row["correct"].strip().lower() not in {
            "a", "b", "c", "d"
        }:
            raise ValueError(
                f"{course_code}: invalid correct answer "
                f"for {question_id}"
            )

        for option in ("option_a", "option_b", "option_c", "option_d"):
            if len(row[option]) > 500:
                raise ValueError(
                    f"{course_code}: option too long "
                    f"for question {question_id}"
                )

    return {
        "course_code": course_code,
        "title": course_title,
        "description": syllabus.get("description"),
        "category_code": category_code,
        "category_name": CATEGORY_NAMES[category_code],
        "prerequisites": syllabus.get("prerequisites"),
        "checkpoints": syllabus.get("checkpoints"),
        "topics": topics,
        "questions": questions,
    }


# --------------------------------------------------
# LOAD AND VALIDATE ALL COURSES
# --------------------------------------------------

def load_all_courses():
    if not ROOT.is_dir():
        raise FileNotFoundError(
            f"Course source directory not found: {ROOT}"
        )

    syllabus_files = sorted(ROOT.rglob("syllabus.json"))

    if len(syllabus_files) != EXPECTED_COURSES:
        raise ValueError(
            f"Expected {EXPECTED_COURSES} courses, "
            f"found {len(syllabus_files)}"
        )

    courses = [
        load_course(path.parent)
        for path in syllabus_files
    ]

    course_codes = [
        course["course_code"] for course in courses
    ]

    if len(course_codes) != len(set(course_codes)):
        raise ValueError("Duplicate course codes found")

    return courses


# --------------------------------------------------
# DATABASE IMPORT
# --------------------------------------------------

def import_courses(db: Session, courses: list):
    for data in courses:

        # Get or create category
        category = (
            db.query(Category)
            .filter(
                Category.category_code == data["category_code"]
            )
            .first()
        )

        if not category:
            category = Category(
                category_code=data["category_code"],
                name=data["category_name"],
            )
            db.add(category)
            db.flush()

        # Skip an already imported course
        existing_course = (
            db.query(Course)
            .filter(
                Course.course_code == data["course_code"]
            )
            .first()
        )

        if existing_course:
            print(
                f"SKIPPED existing course: "
                f"{data['course_code']}"
            )
            continue

        course = Course(
            course_code=data["course_code"],
            title=data["title"],
            description=data["description"],
            category_id=category.id,
            prerequisites=data["prerequisites"],
            checkpoints=data["checkpoints"],
        )

        db.add(course)
        db.flush()

        # Create topics and their quizzes
        topic_map = {}

        for topic_data in data["topics"]:
            topic = Topic(
                title=topic_data["title"],
                description=topic_data["description"],
                course_id=course.id,
                sequence_number=topic_data["sequence_number"],
                source_topic_id=topic_data["source_topic_id"],
                difficulty_level=topic_data["difficulty_level"],
                subtopics=topic_data["subtopics"],
                prerequisites=topic_data["prerequisites"],
            )

            db.add(topic)
            db.flush()

            topic_map[topic_data["source_topic_id"]] = {
                "id": topic.id,
                "title": topic.title,
                "description": topic.description,
            }

            quiz = Quiz(
                title=f"{topic.title} Quiz",
                description=(
                    f"Assessment for {topic.title}"
                ),
                topic_id=topic.id,
            )

            db.add(quiz)
            db.flush()

            topic_map[topic_data["source_topic_id"]][
                "quiz_id"
            ] = quiz.id

            TOTALS["topics"] += 1
            TOTALS["quizzes"] += 1

        # Create questions
        for row in data["questions"]:
            topic_info = topic_map[row["topic"].strip()]

            question = Question(
                quiz_id=topic_info["quiz_id"],
                question_text=row["question"].strip(),
                option_a=row["option_a"].strip(),
                option_b=row["option_b"].strip(),
                option_c=row["option_c"].strip(),
                option_d=row["option_d"].strip(),
                correct_option=row["correct"].strip().upper(),
                source_question_id=row["question_id"].strip(),
                difficulty_level=row["difficulty"].strip().lower(),
                explanation=row["explanation"].strip(),
            )

            db.add(question)
            TOTALS["questions"] += 1

        TOTALS["courses"] += 1

        print(
            f"PREPARED: {data['course_code']} - "
            f"{data['title']}"
        )


# --------------------------------------------------
# MAIN
# --------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Import Learnova curriculum courses"
    )

    parser.add_argument(
        "--commit",
        action="store_true",
        help="Actually insert the validated data",
    )

    args = parser.parse_args()

    print("\n========== LEARNOVA COURSE IMPORT ==========\n")

    try:
        courses = load_all_courses()

        total_topics = sum(
            len(course["topics"]) for course in courses
        )

        total_questions = sum(
            len(course["questions"]) for course in courses
        )

        print("SOURCE VALIDATION SUCCESSFUL")
        print(f"Courses: {len(courses)}")
        print(f"Topics: {total_topics}")
        print(f"Quizzes to create: {total_topics}")
        print(f"Questions: {total_questions}")

        if not args.commit:
            print(
                "\nDRY RUN COMPLETE. "
                "No database records were inserted."
            )
            print(
                "Run with --commit only after reviewing "
                "the validation results."
            )
            return

        db = SessionLocal()

        try:
            with db.begin():
                import_courses(db, courses)

            print("\nDATABASE IMPORT COMMITTED SUCCESSFULLY")

        except Exception:
            db.rollback()
            raise

        finally:
            db.close()

        print("\n========== IMPORT SUMMARY ==========")
        for name, count in TOTALS.items():
            print(f"{name.capitalize()}: {count}")

    except Exception as error:
        print(f"\nIMPORT FAILED: {error}")
        sys.exit(1)


if __name__ == "__main__":
    main()
