"""体脂/体重/围度记录。对应 data-model.md body_metric。"""
from datetime import date as date_t

from sqlalchemy import BigInteger, Date, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class BodyMetric(Base):
    __tablename__ = "body_metric"

    id: Mapped[int] = mapped_column(BigInteger().with_variant(Integer, "sqlite"), primary_key=True)
    student_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("student.id", ondelete="CASCADE"), index=True)
    date: Mapped[date_t] = mapped_column(Date, index=True)
    weight_kg: Mapped[float | None] = mapped_column(Float, nullable=True)
    body_fat_pct: Mapped[float | None] = mapped_column(Float, nullable=True)
    waist_cm: Mapped[float | None] = mapped_column(Float, nullable=True)
    chest_cm: Mapped[float | None] = mapped_column(Float, nullable=True)
    arm_cm: Mapped[float | None] = mapped_column(Float, nullable=True)
    source: Mapped[str] = mapped_column(String(10), default="coach")  # coach / student
    note: Mapped[str | None] = mapped_column(Text, nullable=True)
