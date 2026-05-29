"""学员打卡 + 教练点评（精简）。完整 check_in_set/逐组对比留后续。"""
from datetime import date as date_t, datetime

from sqlalchemy import BigInteger, Boolean, Date, DateTime, ForeignKey, Integer, JSON, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class CheckIn(Base):
    __tablename__ = "check_in"

    id: Mapped[int] = mapped_column(BigInteger().with_variant(Integer, "sqlite"), primary_key=True)
    student_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("student.id", ondelete="CASCADE"), index=True)
    coach_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("coach.id", ondelete="CASCADE"), index=True)
    plan_title: Mapped[str] = mapped_column(String(128))
    date: Mapped[date_t] = mapped_column(Date, index=True)
    feeling: Mapped[int | None] = mapped_column(Integer, nullable=True)  # 1-5
    rpe: Mapped[int | None] = mapped_column(Integer, nullable=True)      # 1-10
    note: Mapped[str | None] = mapped_column(Text, nullable=True)
    sets_detail: Mapped[list] = mapped_column(JSON, default=list)        # [{exercise,prescribed,actual:[...]}]
    commented: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class CoachComment(Base):
    __tablename__ = "coach_comment"

    id: Mapped[int] = mapped_column(BigInteger().with_variant(Integer, "sqlite"), primary_key=True)
    check_in_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("check_in.id", ondelete="CASCADE"), index=True)
    coach_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("coach.id", ondelete="CASCADE"), index=True)
    text: Mapped[str] = mapped_column(Text)
    image_urls: Mapped[list] = mapped_column(JSON, default=list)  # E6 配图
    voice_url: Mapped[str | None] = mapped_column(Text, nullable=True)  # MVP+1
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
