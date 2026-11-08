from pydantic import BaseModel, Field
from typing import Literal

class QuestionCreate(BaseModel):
    question_text: str = Field(min_length=5)
    option_a: str = Field(min_length=1, max_length=500)
    option_b: str = Field(min_length=1, max_length=500)
    option_c: str = Field(min_length=1, max_length=500)
    option_d: str = Field(min_length=1, max_length=500)
    correct_option: Literal["A", "B", "C", "D"]


class QuestionResponse(BaseModel):
    id: int
    quiz_id: int
    question_text: str
    option_a: str
    option_b: str
    option_c: str
    option_d: str

    model_config = {"from_attributes": True}
