from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.models.learning_progress import LearningProgress
from app.models.learning_material import LearningMaterial
from app.schemas.learning_progress import LearningProgressUpdate


def update_learning_progress(
    db: Session,
    user_id: int,
    learning_material_id: int,
    progress_data: LearningProgressUpdate
):
    # Check whether the learning material exists
    material = db.query(LearningMaterial).filter(
        LearningMaterial.id == learning_material_id
    ).first()

    if not material:
        raise LookupError("Learning material not found")

    # Find existing progress record
    progress = db.query(LearningProgress).filter(
        LearningProgress.user_id == user_id,
        LearningProgress.learning_material_id == learning_material_id
    ).first()

    now = datetime.now(timezone.utc)
    new_status = progress_data.status

    # Create a record if this is the learner's first update
    if not progress:
        progress = LearningProgress(
            user_id=user_id,
            learning_material_id=learning_material_id,
            status="not_started"
        )
        db.add(progress)

    # Update timestamps based on the new status
    if new_status == "not_started":
        progress.started_at = None
        progress.completed_at = None

    elif new_status == "in_progress":
        if progress.started_at is None:
            progress.started_at = now
        progress.completed_at = None

    elif new_status == "completed":
        if progress.started_at is None:
            progress.started_at = now

        if progress.status != "completed":
            progress.completed_at = now

    progress.status = new_status

    db.commit()
    db.refresh(progress)

    return progress


def get_progress_by_material(
    db: Session,
    user_id: int,
    learning_material_id: int
):
    return db.query(LearningProgress).filter(
        LearningProgress.user_id == user_id,
        LearningProgress.learning_material_id == learning_material_id
    ).first()


def get_all_progress_by_user(
    db: Session,
    user_id: int
):
    return db.query(LearningProgress).filter(
        LearningProgress.user_id == user_id
    ).all()
