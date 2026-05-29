"""动作库。MVP 全部系统预置只读（coach_id IS NULL）；自建留 MVP+1。
target_muscle 用 {primary,secondary}（v4 E1 解剖图）。"""
from sqlalchemy import BigInteger, Integer, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Exercise(Base):
    __tablename__ = "exercise"

    id: Mapped[int] = mapped_column(BigInteger().with_variant(Integer, "sqlite"), primary_key=True)
    name: Mapped[str] = mapped_column(String(64), index=True)
    category: Mapped[str] = mapped_column(String(20), default="strength")  # strength/cardio/mobility
    target_primary: Mapped[list] = mapped_column(JSON, default=list)       # ["股四头肌","臀大肌"]
    target_secondary: Mapped[list] = mapped_column(JSON, default=list)
    demo_video_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    cues: Mapped[str | None] = mapped_column(Text, nullable=True)          # 动作要领
    is_preset: Mapped[bool] = mapped_column(default=True)
