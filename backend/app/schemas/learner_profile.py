from pydantic import BaseModel, Field
from typing import Literal


class LearnerProfileCreate(BaseModel):
    learner_category: Literal[
        "college_student",
        "self_learner",
        "placement_learner"
    ]

    current_level: Literal[
        "beginner",
        "intermediate",
        "advanced"
    ]

    daily_study_minutes: int = Field(
        ge=1,
        le=1440
    )

    learning_goal: str = Field(
        min_length=3,
        max_length=500
    )

    interests: str | None = None

    course_id: int = Field(gt=0)


class LearnerProfileUpdate(BaseModel):
    learner_category: Literal[
        "college_student",
        "self_learner",
        "placement_learner"
    ] | None = None

    current_level: Literal[
        "beginner",
        "intermediate",
        "advanced"
    ] | None = None

    daily_study_minutes: int | None = Field(
        default=None,
        ge=1,
        le=1440
    )

    learning_goal: str | None = Field(
        default=None,
        min_length=3,
        max_length=500
    )

    interests: str | None = None

    course_id: int | None = Field(
        default=None,
        gt=0
    )


class LearnerProfileResponse(BaseModel):
    id: int
    user_id: int
    learner_category: str
    current_level: str
    daily_study_minutes: int
    learning_goal: str
    interests: str | None
    course_id: int

    model_config = {"from_attributes": True}