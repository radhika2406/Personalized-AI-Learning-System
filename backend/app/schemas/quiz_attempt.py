
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


class QuestionReviewResponse(BaseModel):
    question_id: int
    question_text: str
    option_a: str
    option_b: str
    option_c: str
    option_d: str
    selected_option: str
    correct_option: str
    is_correct: bool
    explanation: str | None = None


class QuizResultResponse(BaseModel):
    attempt_id: int
    quiz_id: int
    score: int
    total_questions: int
    percentage: float
    submitted_at: datetime
    review: list[QuestionReviewResponse]


class QuizAttemptReviewResponse(BaseModel):
    attempt_id: int
    quiz_id: int
    score: int
    total_questions: int
    percentage: float
    submitted_at: datetime
    review: list[QuestionReviewResponse]
