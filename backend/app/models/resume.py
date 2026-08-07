from __future__ import annotations
from typing import TYPE_CHECKING
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.database import Base


class Resume(Base):
    """Uploaded resume metadata and parsed content."""

    __tablename__ = "resumes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
    )
    filename: Mapped[str] = mapped_column(String(255), nullable=False)
    file_path: Mapped[str] = mapped_column(String(500), nullable=False)
    parsed_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    upload_date: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
    )
    if TYPE_CHECKING:
        from app.models.user import User
    # Each resume belongs to exactly one user account.
    user: Mapped["User"] = relationship("User", back_populates="resumes")
