"""鉴权端点。
- 教练：手机号 + 密码 → JWT
- 学员：wx.login 的 code → code2session → 自家 JWT（仍为骨架）"""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import create_access_token, verify_password
from app.db.session import get_db
from app.models import Coach

router = APIRouter()


class CoachLoginIn(BaseModel):
    phone: str
    password: str


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"


@router.post("/coach/login", response_model=TokenOut)
async def coach_login(body: CoachLoginIn, db: AsyncSession = Depends(get_db)) -> TokenOut:
    coach = (await db.execute(select(Coach).where(Coach.phone == body.phone))).scalar_one_or_none()
    if coach is None or not verify_password(body.password, coach.password_hash):
        raise HTTPException(status_code=401, detail="手机号或密码错误")
    return TokenOut(access_token=create_access_token(subject=f"coach:{coach.id}", role="coach"))


class WxLoginIn(BaseModel):
    code: str


@router.post("/student/wx-login", response_model=TokenOut)
async def student_wx_login(body: WxLoginIn) -> TokenOut:
    # TODO: httpx 调 code2session(appid, secret, code) → openid → upsert student → JWT
    raise HTTPException(status_code=501, detail="wx-login not implemented yet")
