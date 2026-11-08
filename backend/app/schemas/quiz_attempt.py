from datetime import datetime
from pydantic import BaseModel, Field


class QuizAnswerSubmit(BaseModel):
    question_id: int = Field(gt=0)
    selected_option: str = Field(pattern="^[A-D]$")


class QuizSubmission(BaseModel):
    answers: list[QuizAnswerSubmit] = Field(min_length=1)


class QuizAttemptResponse(BaseModel):
    id: int
    quiz_id: int
    score: int
    total_questions: int
    started_at: datetime
    submitted_at: datetime | None

    model_config = {"from_attributes": True}


class QuizResultResponse(BaseModel):
    attempt_id: int
    quiz_id: int
    score: int
    total_questions: int
    percentage: float
    submitted_at: datetime
