from datetime import datetime, timezone

from sqlalchemy import String, Text, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class LearningMaterial(Base):
    __tablename__ = "learning_materials"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    title: Mapped[str] = mapped_column(String(200), nullable=False)

    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    material_type: Mapped[str] = mapped_column(String(30), nullable=False)

    content_text: Mapped[str | None] = mapped_column(Text, nullable=True)

    content_url: Mapped[str | None] = mapped_column(String(500), nullable=True)

    topic_id: Mapped[int] = mapped_column(
        ForeignKey("topics.id"),
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )
