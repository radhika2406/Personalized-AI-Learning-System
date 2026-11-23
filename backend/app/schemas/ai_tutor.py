from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field, field_validator


class AIChatRequest(BaseModel):
    message: str = Field(
        min_length=1,
        max_length=10000
    )

    @field_validator("message")
    @classmethod
    def validate_message(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("Message cannot be empty.")

        return value

    conversation_id: int | None = Field(
        default=None,
        gt=0
    )

    course_id: int | None = Field(
        default=None,
        gt=0
    )

    topic_id: int | None = Field(
        default=None,
        gt=0
    )


class AIMessageResponse(BaseModel):
    id: int
    conversation_id: int
    role: Literal["user", "assistant"]
    content: str
    created_at: datetime

    model_config = {"from_attributes": True}


class AIConversationResponse(BaseModel):
    id: int
    user_id: int
    course_id: int | None
    topic_id: int | None
    title: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class AIConversationDetailResponse(AIConversationResponse):
    messages: list[AIMessageResponse]


class AIChatResponse(BaseModel):
    conversation_id: int
    user_message: AIMessageResponse
    assistant_message: AIMessageResponse
