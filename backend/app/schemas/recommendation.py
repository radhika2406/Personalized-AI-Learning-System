from datetime import datetime

from pydantic import BaseModel, Field


class RecommendationCreate(BaseModel):
    course_id: int | None = Field(default=None, gt=0)
    topic_id: int | None = Field(default=None, gt=0)

    recommendation_type: str = Field(
        min_length=2,
        max_length=30
    )

    title: str = Field(
        min_length=2,
        max_length=200
    )

    description: str = Field(min_length=1)

    reason: str | None = None

    priority: int = Field(default=1, ge=1)


class RecommendationResponse(BaseModel):
    id: int
    user_id: int
    course_id: int | None
    topic_id: int | None
    recommendation_type: str
    title: str
    description: str
    reason: str | None
    priority: int
    status: str
    created_at: datetime

    model_config = {"from_attributes": True}
    