
from sqlalchemy.orm import Session

from app.models.course import Course
from app.models.course_enrollment import CourseEnrollment


def _enrollment_response(enrollment, course):
    return {
        "id": enrollment.id,
        "user_id": enrollment.user_id,
        "course_id": enrollment.course_id,
        "course_title": course.title,
        "enrolled_at": enrollment.enrolled_at,
    }


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

    return _enrollment_response(enrollment, course), None


def get_user_enrollments(
    db: Session,
    user_id: int
):
    results = (
        db.query(CourseEnrollment, Course)
        .join(
            Course,
            Course.id == CourseEnrollment.course_id
        )
        .filter(CourseEnrollment.user_id == user_id)
        .order_by(CourseEnrollment.enrolled_at.desc())
        .all()
    )

    return [
        _enrollment_response(enrollment, course)
        for enrollment, course in results
    ]


def get_user_course_enrollment(
    db: Session,
    user_id: int,
    course_id: int
):
    result = (
        db.query(CourseEnrollment, Course)
        .join(
            Course,
            Course.id == CourseEnrollment.course_id
        )
        .filter(
            CourseEnrollment.user_id == user_id,
            CourseEnrollment.course_id == course_id
        )
        .first()
    )

    if not result:
        return None

    enrollment, course = result

    return _enrollment_response(enrollment, course)


def unenroll_user_from_course(
    db: Session,
    user_id: int,
    course_id: int
):
    enrollment = db.query(CourseEnrollment).filter(
        CourseEnrollment.user_id == user_id,
        CourseEnrollment.course_id == course_id
    ).first()

    if not enrollment:
        return False

    db.delete(enrollment)
    db.commit()

    return True
