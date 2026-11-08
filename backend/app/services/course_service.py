from sqlalchemy.orm import Session

from app.models.course import Course
from app.schemas.course import CourseCreate


def create_course(db: Session, course_data: CourseCreate) -> Course:
    existing_course = (
        db.query(Course)
        .filter(Course.course_code == course_data.course_code)
        .first()
    )

    if existing_course:
        raise ValueError("Course code already exists")

    new_course = Course(
        course_code=course_data.course_code,
        title=course_data.title,
        description=course_data.description,
    )

    db.add(new_course)
    db.commit()
    db.refresh(new_course)

    return new_course


def get_all_courses(db: Session) -> list[Course]:
    return db.query(Course).order_by(Course.id).all()


def get_course_by_id(db: Session, course_id: int) -> Course | None:
    return db.query(Course).filter(Course.id == course_id).first()