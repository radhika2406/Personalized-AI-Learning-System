from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field

from app.db.database import get_db
from app.models.user import User
from app.core.security import get_current_user
from app.schemas.recommendation import (
    RecommendationCreate,
    RecommendationResponse,
)
from app.services.recommendation_service import (
    create_recommendation,
    get_user_recommendations,
    get_recommendation_by_id,
    update_recommendation_status,
)

router = APIRouter(
    prefix="/recommendations",
    tags=["Recommendations"],
)


class RecommendationStatusUpdate(BaseModel):
    status: str = Field(
        pattern="^(pending|accepted|completed|dismissed)$"
    )


@router.post(
    "/",
    response_model=RecommendationResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_new_recommendation(
    recommendation_data: RecommendationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_recommendation(
        db,
        current_user.id,
        recommendation_data,
    )


@router.get(
    "/me",
    response_model=list[RecommendationResponse],
)
def list_my_recommendations(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_user_recommendations(
        db,
        current_user.id,
    )


@router.get(
    "/{recommendation_id}",
    response_model=RecommendationResponse,
)
def get_my_recommendation(
    recommendation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    recommendation = get_recommendation_by_id(
        db,
        recommendation_id,
        current_user.id,
    )

    if not recommendation:
        raise HTTPException(
            status_code=404,
            detail="Recommendation not found",
        )

    return recommendation


@router.patch(
    "/{recommendation_id}/status",
    response_model=RecommendationResponse,
)
def update_my_recommendation_status(
    recommendation_id: int,
    status_data: RecommendationStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    recommendation = get_recommendation_by_id(
        db,
        recommendation_id,
        current_user.id,
    )

    if not recommendation:
        raise HTTPException(
            status_code=404,
            detail="Recommendation not found",
        )

    return update_recommendation_status(
        db,
        recommendation,
        status_data.status,
    )