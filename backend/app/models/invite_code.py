"""邀请码：跨租户表（学员输码 → 反查 coach_id）。
部署红线：此表**不开 RLS**，否则学员无法跨租户匹配教练（见 deployment.md）。"""
from datetime import datetime

from sqlalchemy import BigInteger, Integer, DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class InviteCode(Base):
    __tablename__ = "invite_codes"  # 复数：与 RLS 例外表约定一致

    id: Mapped[int] = mapped_column(BigInteger().with_variant(Integer, "sqlite"), primary_key=True)
    code: Mapped[str] = mapped_column(String(16), unique=True, index=True)
    coach_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("coach.id", ondelete="CASCADE"), index=True
    )
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    used_count: Mapped[int] = mapped_column(BigInteger, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
