from datetime import datetime

from pydantic import BaseModel


class CourseEnrollmentResponse(BaseModel):
    id: int
    user_id: int
    course_id: int
    enrolled_at: datetime

    model_config = {"from_attributes": True}