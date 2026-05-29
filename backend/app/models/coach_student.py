"""教练-学员关系。对应 data-model.md 表 3 `coach_student`（含 v5 服务台账/健康备忘/标签）。"""
from datetime import date, datetime

from sqlalchemy import (BigInteger, Date, DateTime, ForeignKey, Integer, JSON,
                        String, Text, UniqueConstraint, func)
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class CoachStudent(Base):
    __tablename__ = "coach_student"
    __table_args__ = (UniqueConstraint("coach_id", "student_id", name="uq_coach_student"),)

    id: Mapped[int] = mapped_column(BigInteger().with_variant(Integer, "sqlite"), primary_key=True)
    coach_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("coach.id", ondelete="CASCADE"), index=True)
    student_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("student.id", ondelete="CASCADE"), index=True)
    alias: Mapped[str | None] = mapped_column(String(64), nullable=True)
    goal: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(20), default="active")   # active/trial/paused/pending_renewal/expired/churned
    source: Mapped[str] = mapped_column(String(20), default="private")  # private/gym_assigned/referral/trial_class/other
    tags: Mapped[list] = mapped_column(JSON, default=list)              # [{"name":"增肌","color":"cyan"}]
    joined_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    coaching_started_at: Mapped[date | None] = mapped_column(Date, nullable=True)   # v5 H2
    ended_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    ended_reason: Mapped[str | None] = mapped_column(String(40), nullable=True)     # v5 H3
    # 服务台账 v5 S4（手动维护，不接支付）
    next_due_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    remaining_sessions: Mapped[int | None] = mapped_column(Integer, nullable=True)
    lifetime_paid_yuan: Mapped[int] = mapped_column(Integer, default=0)
    current_period_paid_yuan: Mapped[int] = mapped_column(Integer, default=0)
    # 健康备忘 v5 S3
    health_notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    contraindicated_exercise_ids: Mapped[list] = mapped_column(JSON, default=list)
