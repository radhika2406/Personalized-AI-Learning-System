from sqlalchemy.orm import Session

from app.models.learner_profile import LearnerProfile
from app.models.course import Course
from app.schemas.learner_profile import (
    LearnerProfileCreate,
    LearnerProfileUpdate,
)


def create_learner_profile(
    db: Session,
    user_id: int,
    profile_data: LearnerProfileCreate,
):
    existing_profile = (
        db.query(LearnerProfile)
        .filter(LearnerProfile.user_id == user_id)
        .first()
    )

    if existing_profile:
        raise ValueError("Learner profile already exists")

    # Validate course only when a database course is selected.
    if profile_data.course_id is not None:
        course = (
            db.query(Course)
            .filter(Course.id == profile_data.course_id)
            .first()
        )

        if not course:
            raise LookupError("Course not found")

    new_profile = LearnerProfile(
        user_id=user_id,
        **profile_data.model_dump(),
    )

    try:
        db.add(new_profile)
        db.commit()
        db.refresh(new_profile)
        return new_profile
    except Exception:
        db.rollback()
        raise


def get_learner_profile_by_user(
    db: Session,
    user_id: int,
):
    return (
        db.query(LearnerProfile)
        .filter(LearnerProfile.user_id == user_id)
        .first()
    )


def update_learner_profile(
    db: Session,
    user_id: int,
    profile_data: LearnerProfileUpdate,
):
    profile = get_learner_profile_by_user(db, user_id)

    if not profile:
        raise LookupError("Learner profile not found")

    update_data = profile_data.model_dump(exclude_unset=True)

    # Validate a course only when a non-null course ID is supplied.
    if update_data.get("course_id") is not None:
        course = (
            db.query(Course)
            .filter(Course.id == update_data["course_id"])
            .first()
        )

        if not course:
            raise LookupError("Course not found")

    for field, value in update_data.items():
        setattr(profile, field, value)

    try:
        db.commit()
        db.refresh(profile)
        return profile
    except Exception:
        db.rollback()
        raise
