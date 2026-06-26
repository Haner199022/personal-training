"""鉴权端点。教练手机号+密码；学员 wx.login code → JWT。"""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.core.security import create_access_token, verify_password
from app.db.session import get_db
from app.models import Coach, Student

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
async def student_wx_login(body: WxLoginIn, db: AsyncSession = Depends(get_db)) -> TokenOut:
    """生产：httpx 调 code2session(appid, secret, code) → openid。
    dev（未配 WX_APP_SECRET）：映射到种子学员 demo_openid_1（林楠，已绑定张教练），让小程序能跑通。"""
    settings = get_settings()
    if settings.wx_app_secret:
        raise HTTPException(status_code=501, detail="real code2session not wired yet")
    openid = "demo_openid_1"
    student = (await db.execute(select(Student).where(Student.wx_openid == openid))).scalar_one_or_none()
    if student is None:
        student = Student(wx_openid=openid, display_name="体验学员")
        db.add(student)
        await db.commit()
        await db.refresh(student)
    return TokenOut(access_token=create_access_token(subject=f"student:{student.id}", role="student"))
