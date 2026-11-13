from pydantic import BaseModel, Field


class CourseCreate(BaseModel):
    course_code: str = Field(min_length=2, max_length=20)
    title: str = Field(min_length=2, max_length=150)
    description: str | None = None


class CategoryInfo(BaseModel):
    id: int
    category_code: str
    name: str

    model_config = {"from_attributes": True}


class CourseResponse(BaseModel):
    id: int
    course_code: str
    title: str
    description: str | None
    category_id: int | None = None
    category: CategoryInfo | None = None

    model_config = {"from_attributes": True}