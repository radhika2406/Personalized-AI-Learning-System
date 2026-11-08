from datetime import datetime, timezone

from sqlalchemy import Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class TopicMastery(Base):
    __tablename__ = "topic_mastery"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )

    topic_id: Mapped[int] = mapped_column(
        ForeignKey("topics.id"),
        nullable=False
    )

    mastery_score: Mapped[float] = mapped_column(
        Float,
        default=0.0,
        nullable=False
    )

    quizzes_attempted: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False
    )

    last_assessed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )