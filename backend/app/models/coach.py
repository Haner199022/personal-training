"""教练账号。对应 vault data-model.md 表 1 `coach`（MVP + v5 IP 主页/阈值字段）。"""
from datetime import datetime

from sqlalchemy import BigInteger, Boolean, DateTime, Integer, JSON, LargeBinary, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Coach(Base):
    __tablename__ = "coach"

    id: Mapped[int] = mapped_column(BigInteger().with_variant(Integer, "sqlite"), primary_key=True)
    phone: Mapped[str] = mapped_column(String(20), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    display_name: Mapped[str] = mapped_column(String(64))
    avatar_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    bio: Mapped[str | None] = mapped_column(Text, nullable=True)
    cert_tags: Mapped[list] = mapped_column(JSON, default=list)              # ["NSCA-CPT", ...]
    subscription_tier: Mapped[str] = mapped_column(String(20), default="free")
    affiliated_studio: Mapped[str | None] = mapped_column(String(128), nullable=True)  # v5 P2-26
    profile_intro_rich: Mapped[str | None] = mapped_column(Text, nullable=True)        # v5 S8
    profile_published: Mapped[bool] = mapped_column(Boolean, default=False)            # v5 S8
    favorite_exercise_ids: Mapped[list] = mapped_column(JSON, default=list)            # v5 P2-20
    risk_days_threshold: Mapped[int] = mapped_column(Integer, default=5)               # v5 C6
    push_subscribe_enabled: Mapped[bool] = mapped_column(Boolean, default=True)        # ADR-0015 主推
    push_inbox_enabled: Mapped[bool] = mapped_column(Boolean, default=True)            # 站内信兜底
    enterprise_wechat_webhook: Mapped[bytes | None] = mapped_column(LargeBinary, nullable=True)  # 加密
    first_login_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
