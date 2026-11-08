from datetime import datetime

from pydantic import BaseModel


class TopicMasteryResponse(BaseModel):
    id: int
    user_id: int
    topic_id: int
    mastery_score: float
    quizzes_attempted: int
    last_assessed_at: datetime | None

    model_config = {"from_attributes": True}