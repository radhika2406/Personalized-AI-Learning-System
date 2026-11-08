from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.user import User
from app.core.security import get_current_user
from app.schemas.topic import TopicCreate, TopicResponse
from app.services.topic_service import (
    create_topic,
    get_topics_by_course,
    get_topic_by_id,
)

router = APIRouter(prefix="/topics", tags=["Topics"])


@router.post("/", response_model=TopicResponse, status_code=status.HTTP_201_CREATED)
def create_new_topic(
    topic_data: TopicCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return create_topic(db, topic_data)
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error))


@router.get("/course/{course_id}", response_model=list[TopicResponse])
def list_course_topics(
    course_id: int,
    db: Session = Depends(get_db),
):
    return get_topics_by_course(db, course_id)


@router.get("/{topic_id}", response_model=TopicResponse)
def get_topic(
    topic_id: int,
    db: Session = Depends(get_db),
):
    topic = get_topic_by_id(db, topic_id)

    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")

    return topic
