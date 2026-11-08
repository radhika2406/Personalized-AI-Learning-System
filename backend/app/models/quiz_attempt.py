from datetime import datetime, timezone

from sqlalchemy import Integer, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class QuizAttempt(Base):
    __tablename__ = "quiz_attempts"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )

    quiz_id: Mapped[int] = mapped_column(
        ForeignKey("quizzes.id"),
        nullable=False
    )

    score: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0
    )

    total_questions: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    submitted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )
