from sqlalchemy.orm import Session

from app.models.course import Course
from app.models.course_enrollment import CourseEnrollment


def enroll_user_in_course(
    db: Session,
    user_id: int,
    course_id: int
):
    course = db.query(Course).filter(
        Course.id == course_id
    ).first()

    if not course:
        return None, "Course not found"

    existing_enrollment = db.query(CourseEnrollment).filter(
        CourseEnrollment.user_id == user_id,
        CourseEnrollment.course_id == course_id
    ).first()

    if existing_enrollment:
        return None, "Already enrolled in this course"

    enrollment = CourseEnrollment(
        user_id=user_id,
        course_id=course_id
    )

    db.add(enrollment)
    db.commit()
    db.refresh(enrollment)

    return enrollment, None


def get_user_enrollments(
    db: Session,
    user_id: int
):
    return db.query(CourseEnrollment).filter(
        CourseEnrollment.user_id == user_id
    ).order_by(CourseEnrollment.enrolled_at.desc()).all()


def get_user_course_enrollment(
    db: Session,
    user_id: int,
    course_id: int
):
    return db.query(CourseEnrollment).filter(
        CourseEnrollment.user_id == user_id,
        CourseEnrollment.course_id == course_id
    ).first()


def unenroll_user_from_course(
    db: Session,
    user_id: int,
    course_id: int
):
    enrollment = get_user_course_enrollment(
        db=db,
        user_id=user_id,
        course_id=course_id
    )

    if not enrollment:
        return False

    db.delete(enrollment)
    db.commit()

    return True