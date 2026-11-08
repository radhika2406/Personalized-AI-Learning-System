from datetime import datetime
from typing import Literal

from pydantic import BaseModel


class LearningProgressUpdate(BaseModel):
    status: Literal[
        "not_started",
        "in_progress",
        "completed"
    ]


class LearningProgressResponse(BaseModel):
    id: int
    user_id: int
    learning_material_id: int
    status: str
    started_at: datetime | None
    completed_at: datetime | None
    updated_at: datetime

    model_config = {"from_attributes": True}
