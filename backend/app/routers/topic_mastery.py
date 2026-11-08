from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.core.security import get_current_user
from app.schemas.topic_mastery import TopicMasteryResponse
from app.services import topic_mastery_service


router = APIRouter(
    prefix="/topic-mastery",
    tags=["Topic Mastery"]
)


@router.get("/me", response_model=list[TopicMasteryResponse])
def get_my_topic_masteries(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return topic_mastery_service.get_all_user_masteries(
        db=db,
        user_id=current_user.id
    )


@router.get("/{topic_id}", response_model=TopicMasteryResponse)
def get_my_topic_mastery(
    topic_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    mastery = topic_mastery_service.get_user_topic_mastery(
        db=db,
        user_id=current_user.id,
        topic_id=topic_id
    )

    if not mastery:
        raise HTTPException(
            status_code=404,
            detail="Topic mastery not found"
        )

    return mastery