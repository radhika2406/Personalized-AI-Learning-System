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

    content_status: str = Field(
        default="Needs lesson content",
        max_length=50
    )

    resource_verification_status: str = Field(
        default="Needs link verification",
        max_length=50
    )

    topic_id: int = Field(gt=0)


class LearningMaterialResponse(BaseModel):
    id: int
    title: str
    description: str | None
    material_type: str
    content_text: str | None
    content_url: str | None
    content_status: str
    resource_verification_status: str
    topic_id: int

    model_config = {"from_attributes": True}
