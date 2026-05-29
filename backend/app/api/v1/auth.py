"""鉴权端点骨架。
- 教练：手机号 + 密码 → JWT
- 学员：wx.login 的 code → code2session → 自家 JWT
真实实现待接 DB / 微信 API，这里先给可调通的占位 + TODO。"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.core.security import create_access_token

router = APIRouter()


class CoachLoginIn(BaseModel):
    phone: str
    password: str


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"


@router.post("/coach/login", response_model=TokenOut)
async def coach_login(body: CoachLoginIn) -> TokenOut:
    # TODO: 查 coach by phone → verify_password → 取 coach.id
    raise HTTPException(status_code=501, detail="coach login not implemented yet")


class WxLoginIn(BaseModel):
    code: str  # wx.login() 返回的临时 code


@router.post("/student/wx-login", response_model=TokenOut)
async def student_wx_login(body: WxLoginIn) -> TokenOut:
    # TODO: httpx 调 code2session(appid, secret, code) → openid
    #       → upsert student by openid → 签发 JWT
    raise HTTPException(status_code=501, detail="wx-login not implemented yet")
