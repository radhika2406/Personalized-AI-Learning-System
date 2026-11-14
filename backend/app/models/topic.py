
from datetime import datetime, timezone

from sqlalchemy import (
    String,
    Text,
    DateTime,
    ForeignKey,
    Integer,
    JSON,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class Topic(Base):
    __tablename__ = "topics"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    title: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    course_id: Mapped[int] = mapped_column(
        ForeignKey("courses.id"),
        nullable=False,
    )

    sequence_number: Mapped[int] = mapped_column(
        Integer,
        default=1,
        nullable=False,
    )

    source_topic_id: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    difficulty_level: Mapped[str | None] = mapped_column(
        String(30),
        nullable=True,
    )

    subtopics: Mapped[list | None] = mapped_column(
        JSON,
        nullable=True,
    )

    prerequisites: Mapped[list | None] = mapped_column(
        JSON,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
