from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.schemas.learner_profile import (
    LearnerProfileCreate,
    LearnerProfileUpdate,
    LearnerProfileResponse,
)
from app.services.learner_profile_service import (
    create_learner_profile,
    get_learner_profile_by_user,
    update_learner_profile,
)

router = APIRouter(
    prefix="/learner-profiles",
    tags=["Learner Profiles"]
)


@router.post(
    "/",
    response_model=LearnerProfileResponse,
    status_code=status.HTTP_201_CREATED
)
def create_profile(
    profile_data: LearnerProfileCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        return create_learner_profile(
            db=db,
            user_id=current_user.id,
            profile_data=profile_data
        )
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(error)
        )
    except LookupError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error)
        )


@router.get(
    "/me",
    response_model=LearnerProfileResponse
)
def get_my_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    profile = get_learner_profile_by_user(
        db=db,
        user_id=current_user.id
    )

    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Learner profile not found"
        )

    return profile


@router.patch(
    "/me",
    response_model=LearnerProfileResponse
)
def update_my_profile(
    profile_data: LearnerProfileUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        return update_learner_profile(
            db=db,
            user_id=current_user.id,
            profile_data=profile_data
        )
    except LookupError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error)
        )