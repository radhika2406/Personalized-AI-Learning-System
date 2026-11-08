from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.schemas.learning_progress import (
    LearningProgressUpdate,
    LearningProgressResponse
)
from app.services.learning_progress_service import (
    update_learning_progress,
    get_progress_by_material,
    get_all_progress_by_user
)

router = APIRouter(
    prefix="/learning-progress",
    tags=["Learning Progress"]
)


@router.put(
    "/material/{material_id}",
    response_model=LearningProgressResponse
)
def update_progress(
    material_id: int,
    progress_data: LearningProgressUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        return update_learning_progress(
            db=db,
            user_id=current_user.id,
            learning_material_id=material_id,
            progress_data=progress_data
        )
    except LookupError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error)
        )


@router.get(
    "/material/{material_id}",
    response_model=LearningProgressResponse
)
def get_material_progress(
    material_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    progress = get_progress_by_material(
        db=db,
        user_id=current_user.id,
        learning_material_id=material_id
    )

    if not progress:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Learning progress not found"
        )

    return progress


@router.get(
    "/me",
    response_model=list[LearningProgressResponse]
)
def get_my_progress(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_all_progress_by_user(
        db=db,
        user_id=current_user.id
    )
