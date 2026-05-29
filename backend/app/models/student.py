"""学员账号。对应 data-model.md 表 2 `student`。
注意：学员表**不带 coach_id**——一个学员可跟多个教练，关系走 coach_student。"""
from datetime import date, datetime

from sqlalchemy import BigInteger, Date, DateTime, SmallInteger, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Student(Base):
    __tablename__ = "student"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    wx_openid: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    wx_unionid: Mapped[str | None] = mapped_column(String(64), nullable=True)
    display_name: Mapped[str | None] = mapped_column(String(64), nullable=True)
    wx_nickname: Mapped[str | None] = mapped_column(String(64), nullable=True)
    avatar_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    gender: Mapped[int | None] = mapped_column(SmallInteger, nullable=True)  # 0未知 1男 2女
    birth_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    height_cm: Mapped[int | None] = mapped_column(SmallInteger, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
