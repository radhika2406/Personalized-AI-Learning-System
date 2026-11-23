
import csv
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
COURSES_DIR = ROOT / "courses"
OUTPUT_CSV = ROOT / "assessment" / "content" / "topics.csv"
BACKUP_CSV = OUTPUT_CSV.with_suffix(".csv.bak")

FIELDS = [
    "topic_id",
    "course",
    "order",
    "prerequisites",
    "est_minutes",
    "goals",
    "level",
    "interests",
]

DEFAULT_EST_MINUTES = 20
EXPECTED_COURSES = 12
EXPECTED_TOPICS_PER_COURSE = 16


def as_semicolon_text(value):
    if value is None:
        return ""

    if isinstance(value, list):
        return ";".join(str(item).strip() for item in value if str(item).strip())

    return str(value).strip()


def load_existing_metadata():
    if not OUTPUT_CSV.exists():
        return {}

    with OUTPUT_CSV.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)

        if not reader.fieldnames or not set(FIELDS).issubset(reader.fieldnames):
            raise ValueError("Existing topics.csv has unexpected columns.")

        rows = {}

        for row in reader:
            key = (row["course"].strip(), row["topic_id"].strip())

            if key in rows:
                raise ValueError(f"Duplicate existing metadata: {key}")

            rows[key] = {field: row.get(field, "") or "" for field in FIELDS}

        return rows


def generate_metadata():
    syllabus_files = sorted(COURSES_DIR.rglob("syllabus.json"))

    if len(syllabus_files) != EXPECTED_COURSES:
        raise ValueError(
            f"Expected {EXPECTED_COURSES} courses, found {len(syllabus_files)}"
        )

    existing = load_existing_metadata()
    generated = {}

    for syllabus_path in syllabus_files:
        course_dir = syllabus_path.parent
        topics_path = course_dir / "topics.json"

        if not topics_path.exists():
            raise FileNotFoundError(f"Missing file: {topics_path}")

        with syllabus_path.open("r", encoding="utf-8") as file:
            syllabus = json.load(file)

        with topics_path.open("r", encoding="utf-8") as file:
            topics = json.load(file)

        course_code = str(syllabus.get("course_id", "")).strip()

        if not course_code:
            raise ValueError(f"Missing course_id in {syllabus_path}")

        if len(topics) != EXPECTED_TOPICS_PER_COURSE:
            raise ValueError(
                f"{course_code}: expected {EXPECTED_TOPICS_PER_COURSE} topics, "
                f"found {len(topics)}"
            )

        course_topic_ids = {
            str(topic.get("topic_id") or topic.get("id") or "").strip()
            for topic in topics
        }

        if "" in course_topic_ids or len(course_topic_ids) != len(topics):
            raise ValueError(f"{course_code}: missing or duplicate topic IDs")

        for topic in topics:
            topic_id = str(topic.get("topic_id") or topic.get("id") or "").strip()
            key = (course_code, topic_id)

            prerequisites = as_semicolon_text(topic.get("prerequisites"))

            for prerequisite in filter(None, prerequisites.split(";")):
                if prerequisite not in course_topic_ids:
                    raise ValueError(
                        f"{course_code}/{topic_id}: unknown prerequisite "
                        f"{prerequisite}"
                    )

            # Preserve manually curated metadata if this record already exists.
            if key in existing:
                generated[key] = existing[key]
                continue

            generated[key] = {
                "topic_id": topic_id,
                "course": course_code,
                "order": str(topic.get("order", "")),
                "prerequisites": prerequisites,
                "est_minutes": str(
                    topic.get("est_minutes")
                    or topic.get("estimated_minutes")
                    or DEFAULT_EST_MINUTES
                ),
                "goals": as_semicolon_text(topic.get("goals")),
                "level": as_semicolon_text(
                    topic.get("level")
                    or topic.get("difficulty_level")
                    or topic.get("difficulty_stage")
                ),
                "interests": as_semicolon_text(topic.get("interests")),
            }

    if len(generated) != EXPECTED_COURSES * EXPECTED_TOPICS_PER_COURSE:
        raise ValueError(
            f"Expected 192 records, generated {len(generated)}"
        )

    return generated


def main():
    print("\n=== AI TOPIC METADATA GENERATOR ===\n")

    metadata = generate_metadata()

    if OUTPUT_CSV.exists():
        shutil.copy2(OUTPUT_CSV, BACKUP_CSV)
        print(f"Existing CSV backed up to: {BACKUP_CSV}")

    OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)

    with OUTPUT_CSV.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDS)
        writer.writeheader()

        for key in sorted(metadata, key=lambda item: (item[0], int(metadata[item]["order"]))):
            writer.writerow(metadata[key])

    print("\nGENERATION SUCCESSFUL")
    print(f"Courses: {EXPECTED_COURSES}")
    print(f"Topics: {len(metadata)}")
    print(f"Default estimated time: {DEFAULT_EST_MINUTES} minutes")
    print(f"Output: {OUTPUT_CSV}")
    print("\nExisting manually curated records were preserved.")


if __name__ == "__main__":
    main()
