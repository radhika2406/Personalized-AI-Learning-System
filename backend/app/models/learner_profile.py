from datetime import datetime, timezone

from sqlalchemy import (
    String,
    Text,
    Integer,
    DateTime,
    ForeignKey,
    UniqueConstraint,
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

    learner_category: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    current_level: Mapped[str] = mapped_column(
        String(20),
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

    course_id: Mapped[int] = mapped_column(
        ForeignKey("courses.id"),
        nullable=False
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
