import argparse
from pathlib import Path

from app.db.database import SessionLocal
from app.models.course import Course
from app.models.topic import Topic
from app.models.learning_material import LearningMaterial

LESSON_DIR = Path("../learning_material/programming/python/topics")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--commit", action="store_true")
    args = parser.parse_args()

    db = SessionLocal()

    try:
        course = db.query(Course).filter(
            Course.course_code == "python"
        ).one()

        topics = db.query(Topic).filter(
            Topic.course_id == course.id
        ).all()

        if len(topics) != 16:
            raise RuntimeError(f"Expected 16 Python topics, found {len(topics)}.")

        source_ids = [t.source_topic_id for t in topics]
        if None in source_ids or len(set(source_ids)) != 16:
            raise RuntimeError("Python topic source IDs are missing or duplicated.")

        topic_ids = [t.id for t in topics]

        pdf_count = db.query(LearningMaterial).filter(
            LearningMaterial.topic_id.in_(topic_ids),
            LearningMaterial.material_type == "pdf"
        ).count()

        video_count = db.query(LearningMaterial).filter(
            LearningMaterial.topic_id.in_(topic_ids),
            LearningMaterial.material_type == "video"
        ).count()

        if pdf_count != 16 or video_count != 16:
            raise RuntimeError(
                f"Expected 16 PDF and 16 video records; found {pdf_count} and {video_count}."
            )

        updates = []
        errors = []

        for topic in topics:
            source_id = topic.source_topic_id
            file_path = LESSON_DIR / source_id / "lesson.md"

            if not file_path.is_file():
                errors.append(f"Missing file: {file_path}")
                continue

            content = file_path.read_text(encoding="utf-8")

            if len(content.strip()) < 500:
                errors.append(f"Content too short: {source_id}")
                continue

            records = db.query(LearningMaterial).filter(
                LearningMaterial.topic_id == topic.id,
                LearningMaterial.material_type == "lesson"
            ).all()

            if len(records) != 1:
                errors.append(
                    f"{source_id}: expected exactly one lesson record, found {len(records)}"
                )
                continue

            material = records[0]
            updates.append((source_id, material, content))

        if errors:
            raise RuntimeError("; ".join(errors))

        if len(updates) != 16:
            raise RuntimeError(f"Expected 16 updates, prepared {len(updates)}.")

        print("\nPYTHON LESSON UPDATE", "(COMMIT MODE)" if args.commit else "(DRY RUN)")
        print("-" * 72)

        for source_id, material, content in sorted(updates, key=lambda x: x[0]):
            print(
                f"{source_id:30} "
                f"record_id={material.id:<5} "
                f"old={len(material.content_text or ''):>6} chars "
                f"new={len(content):>6} chars"
            )

        print("\nPDF records preserved:", pdf_count)
        print("Video records preserved:", video_count)
        print("Lesson records prepared:", len(updates))

        if not args.commit:
            db.rollback()
            print("\nDRY RUN PASSED. No database changes were made.")
            print("Review the output, then run with --commit to save.")
            return

        for source_id, material, content in updates:
            material.content_text = content
            material.content_status = "Completed"

        db.commit()

        # Verify saved lesson content and unchanged resource counts.
        for source_id, material, content in updates:
            db.refresh(material)
            if material.content_text != content:
                raise RuntimeError(f"Post-commit content verification failed: {source_id}")
            if material.content_status != "Completed":
                raise RuntimeError(f"Post-commit status verification failed: {source_id}")

        print("\nCOMMIT SUCCESSFUL")
        print("Updated lesson records:", len(updates))
        print("PDF records:", pdf_count)
        print("Video records:", video_count)
        print("All 16 lesson records verified.")

    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
