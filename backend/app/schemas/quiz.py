from datetime import datetime
from pydantic import BaseModel, Field


class QuizCreate(BaseModel):
    title: str = Field(
        min_length=2,
        max_length=200
    )

    description: str | None = None

    topic_id: int = Field(gt=0)


class QuizResponse(BaseModel):
    id: int
    title: str
    description: str | None
    topic_id: int
    created_at: datetime

    model_config = {"from_attributes": True}
