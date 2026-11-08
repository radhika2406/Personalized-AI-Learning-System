from datetime import datetime, timezone

from sqlalchemy import (
    String,
    DateTime,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class LearningProgress(Base):
    __tablename__ = "learning_progress"

    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "learning_material_id",
            name="uq_user_learning_material"
        ),
    )

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )

    learning_material_id: Mapped[int] = mapped_column(
        ForeignKey("learning_materials.id"),
        nullable=False
    )

    status: Mapped[str] = mapped_column(
        String(20),
        default="not_started",
        nullable=False
    )

    started_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )

    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False
    )
