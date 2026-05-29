"""训练计划（含 v5 模板）。detail 用 JSON 存课次/动作树，MVP 阶段够灵活。"""
from datetime import date as date_t, datetime

from sqlalchemy import BigInteger, Boolean, Date, DateTime, ForeignKey, Integer, JSON, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class TrainingPlan(Base):
    __tablename__ = "training_plan"

    id: Mapped[int] = mapped_column(BigInteger().with_variant(Integer, "sqlite"), primary_key=True)
    coach_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("coach.id", ondelete="CASCADE"), index=True)
    student_id: Mapped[int | None] = mapped_column(BigInteger, ForeignKey("student.id", ondelete="CASCADE"), nullable=True)
    title: Mapped[str] = mapped_column(String(128))
    goal: Mapped[str | None] = mapped_column(String(255), nullable=True)
    start_date: Mapped[date_t | None] = mapped_column(Date, nullable=True)
    end_date: Mapped[date_t | None] = mapped_column(Date, nullable=True)
    status: Mapped[str] = mapped_column(String(20), default="draft")  # draft/active/template
    is_template: Mapped[bool] = mapped_column(Boolean, default=False)
    template_source_plan_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    detail: Mapped[dict] = mapped_column(JSON, default=dict)  # {"sessions":[{day,title,exercises:[{name,sets,reps,weight,primary}]}]}
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
