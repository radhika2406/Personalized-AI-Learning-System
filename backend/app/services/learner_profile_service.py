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
    profile_data: LearnerProfileCreate
):
    # Check whether the user already has a profile
    existing_profile = db.query(LearnerProfile).filter(
        LearnerProfile.user_id == user_id
    ).first()

    if existing_profile:
        raise ValueError("Learner profile already exists")

    # Check whether the selected course exists
    course = db.query(Course).filter(
        Course.id == profile_data.course_id
    ).first()

    if not course:
        raise LookupError("Course not found")

    # Create the profile
    new_profile = LearnerProfile(
        user_id=user_id,
        learner_category=profile_data.learner_category,
        current_level=profile_data.current_level,
        daily_study_minutes=profile_data.daily_study_minutes,
        learning_goal=profile_data.learning_goal,
        interests=profile_data.interests,
        course_id=profile_data.course_id
    )

    db.add(new_profile)
    db.commit()
    db.refresh(new_profile)

    return new_profile


def get_learner_profile_by_user(
    db: Session,
    user_id: int
):
    return db.query(LearnerProfile).filter(
        LearnerProfile.user_id == user_id
    ).first()


def update_learner_profile(
    db: Session,
    user_id: int,
    profile_data: LearnerProfileUpdate
):
    # Find the learner's existing profile
    profile = get_learner_profile_by_user(db, user_id)

    if not profile:
        raise LookupError("Learner profile not found")

    # Validate the course if course_id is being updated
    update_data = profile_data.model_dump(exclude_unset=True)

    if "course_id" in update_data:
        course = db.query(Course).filter(
            Course.id == update_data["course_id"]
        ).first()

        if not course:
            raise LookupError("Course not found")

    # Apply only submitted fields
    for field, value in update_data.items():
        setattr(profile, field, value)

    db.commit()
    db.refresh(profile)

    return profile