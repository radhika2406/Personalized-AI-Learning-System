from pydantic import BaseModel, Field


class TopicCreate(BaseModel):
    title: str = Field(min_length=2, max_length=150)
    description: str | None = None
    course_id: int = Field(gt=0)
    sequence_number: int = Field(default=1, ge=1)


class TopicResponse(BaseModel):
    id: int
    title: str
    description: str | None
    course_id: int
    sequence_number: int

    model_config = {"from_attributes": True}