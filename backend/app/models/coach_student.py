"""教练-学员关系。对应 data-model.md 表 3 `coach_student`（MVP 取核心列，
v5 的服务台账/健康备忘/标签等字段后续 migration 补）。"""
from datetime import datetime

from sqlalchemy import BigInteger, Integer, DateTime, ForeignKey, String, Text, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class CoachStudent(Base):
    __tablename__ = "coach_student"
    __table_args__ = (UniqueConstraint("coach_id", "student_id", name="uq_coach_student"),)

    id: Mapped[int] = mapped_column(BigInteger().with_variant(Integer, "sqlite"), primary_key=True)
    coach_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("coach.id", ondelete="CASCADE"), index=True
    )
    student_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("student.id", ondelete="CASCADE"), index=True
    )
    alias: Mapped[str | None] = mapped_column(String(64), nullable=True)
    goal: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(20), default="active")
    source: Mapped[str] = mapped_column(String(20), default="private")
    joined_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
