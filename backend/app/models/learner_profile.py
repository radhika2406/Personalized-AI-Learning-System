from datetime import datetime, timezone

from sqlalchemy import (
    String,
    Text,
    Integer,
    DateTime,
    ForeignKey,
    JSON,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class LearnerProfile(Base):
    __tablename__ = "learner_profiles"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        unique=True,
        nullable=False
    )

    # Existing profile fields
    learner_category: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    current_level: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    daily_study_minutes: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    learning_goal: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    interests: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    course_id: Mapped[int | None] = mapped_column(
        ForeignKey("courses.id"),
        nullable=True
    )

    # Additional learning preferences
    education_level: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    daily_study_custom: Mapped[str | None] = mapped_column(
        String(200),
        nullable=True
    )

    learning_goals: Mapped[list | None] = mapped_column(
        JSON,
        nullable=True
    )

    interest_topics: Mapped[list | None] = mapped_column(
        JSON,
        nullable=True
    )

    learning_styles: Mapped[list | None] = mapped_column(
        JSON,
        nullable=True
    )

    preferred_study_days: Mapped[list | None] = mapped_column(
        JSON,
        nullable=True
    )

    preferred_study_schedule: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    course_custom: Mapped[str | None] = mapped_column(
        String(200),
        nullable=True
    )

    learning_target: Mapped[str | None] = mapped_column(
        String(200),
        nullable=True
    )

    # Stores additional write-in answers for individual sections.
    custom_answers: Mapped[dict | None] = mapped_column(
        JSON,
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False
    )
