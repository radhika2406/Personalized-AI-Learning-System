from pydantic import BaseModel, Field, HttpUrl

class LearningMaterialCreate(BaseModel):
    title: str = Field(min_length=2, max_length=200)
    description: str | None = None

    material_type: str = Field(
        min_length=2,
        max_length=30
    )

    content_text: str | None = None
    content_url: HttpUrl | None = None

    topic_id: int = Field(gt=0)


class LearningMaterialResponse(BaseModel):
    id: int
    title: str
    description: str | None
    material_type: str
    content_text: str | None
    content_url: str | None
    topic_id: int

    model_config = {"from_attributes": True}
