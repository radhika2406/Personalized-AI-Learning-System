from pydantic import BaseModel, Field, ConfigDict

class LearnerProfileCreate(BaseModel):
    # Existing fields
    learner_category: str = Field(min_length=2, max_length=100)
    current_level: str = Field(min_length=2, max_length=100)
    daily_study_minutes: int = Field(ge=1, le=1440)
    learning_goal: str = Field(min_length=3, max_length=500)
    interests: str | None = None
    course_id: int | None = Field(default=None, gt=0)

    # Additional preferences
    education_level: str | None = Field(default=None, max_length=100)
    daily_study_custom: str | None = Field(default=None, max_length=200)

    learning_goals: list[str] = Field(default_factory=list)
    interest_topics: list[str] = Field(default_factory=list)
    learning_styles: list[str] = Field(default_factory=list)
    preferred_study_days: list[str] = Field(default_factory=list)

    preferred_study_schedule: str | None = None
    course_custom: str | None = Field(default=None, max_length=200)
    learning_target: str | None = Field(default=None, max_length=200)

    custom_answers: dict[str, str] = Field(default_factory=dict)


class LearnerProfileUpdate(BaseModel):
    # Existing fields
    learner_category: str | None = Field(default=None, min_length=2, max_length=100)
    current_level: str | None = Field(default=None, min_length=2, max_length=100)
    daily_study_minutes: int | None = Field(default=None, ge=1, le=1440)
    learning_goal: str | None = Field(default=None, min_length=3, max_length=500)
    interests: str | None = None
    course_id: int | None = Field(default=None, gt=0)

    # Additional preferences
    education_level: str | None = Field(default=None, max_length=100)
    daily_study_custom: str | None = Field(default=None, max_length=200)

    learning_goals: list[str] | None = None
    interest_topics: list[str] | None = None
    learning_styles: list[str] | None = None
    preferred_study_days: list[str] | None = None

    preferred_study_schedule: str | None = None
    course_custom: str | None = Field(default=None, max_length=200)
    learning_target: str | None = Field(default=None, max_length=200)

    custom_answers: dict[str, str] | None = None


class LearnerProfileResponse(BaseModel):
    id: int
    user_id: int

    learner_category: str
    current_level: str
    daily_study_minutes: int
    learning_goal: str
    interests: str | None
    course_id: int | None

    education_level: str | None
    daily_study_custom: str | None
    learning_goals: list[str] | None
    interest_topics: list[str] | None
    learning_styles: list[str] | None
    preferred_study_days: list[str] | None
    preferred_study_schedule: str | None
    course_custom: str | None
    learning_target: str | None
    custom_answers: dict[str, str] | None

    model_config = ConfigDict(from_attributes=True)
