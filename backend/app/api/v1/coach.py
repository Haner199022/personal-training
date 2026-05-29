"""C-8 设置 / C-9 推送 / C-1 dashboard 聚合 / C-2 邀请码。"""
import secrets
from datetime import date, timedelta

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_coach_id
from app.db.session import get_db
from app.models import CheckIn, Coach, CoachStudent, InviteCode

router = APIRouter(prefix="/coaches")


class ProfileOut(BaseModel):
    display_name: str
    bio: str | None = None
    avatar_url: str | None = None
    cert_tags: list = []
    affiliated_studio: str | None = None
    profile_intro_rich: str | None = None
    profile_published: bool = False
    risk_days_threshold: int = 5
    subscription_tier: str = "free"
    phone_masked: str = ""


@router.get("/me/profile", response_model=ProfileOut)
async def get_profile(coach_id: int = Depends(get_current_coach_id), db: AsyncSession = Depends(get_db)):
    c = await db.get(Coach, coach_id)
    masked = c.phone[:3] + "****" + c.phone[-4:] if len(c.phone) >= 7 else c.phone
    return ProfileOut(
        display_name=c.display_name, bio=c.bio, avatar_url=c.avatar_url, cert_tags=c.cert_tags or [],
        affiliated_studio=c.affiliated_studio, profile_intro_rich=c.profile_intro_rich,
        profile_published=c.profile_published, risk_days_threshold=c.risk_days_threshold,
        subscription_tier=c.subscription_tier, phone_masked=masked,
    )


class ProfileIn(BaseModel):
    display_name: str | None = None
    bio: str | None = None
    cert_tags: list | None = None
    affiliated_studio: str | None = None
    profile_intro_rich: str | None = None
    profile_published: bool | None = None
    risk_days_threshold: int | None = None


@router.put("/me/profile", response_model=ProfileOut)
async def update_profile(body: ProfileIn, coach_id: int = Depends(get_current_coach_id), db: AsyncSession = Depends(get_db)):
    c = await db.get(Coach, coach_id)
    for k, v in body.model_dump(exclude_unset=True).items():
        setattr(c, k, v)
    await db.commit()
    return await get_profile(coach_id, db)


class PushOut(BaseModel):
    subscribe_enabled: bool
    inbox_enabled: bool
    enterprise_wechat_configured: bool


@router.get("/me/push-settings", response_model=PushOut)
async def get_push(coach_id: int = Depends(get_current_coach_id), db: AsyncSession = Depends(get_db)):
    c = await db.get(Coach, coach_id)
    return PushOut(subscribe_enabled=c.push_subscribe_enabled, inbox_enabled=c.push_inbox_enabled,
                   enterprise_wechat_configured=c.enterprise_wechat_webhook is not None)


class PushIn(BaseModel):
    subscribe_enabled: bool | None = None
    inbox_enabled: bool | None = None


@router.put("/me/push-settings", response_model=PushOut)
async def update_push(body: PushIn, coach_id: int = Depends(get_current_coach_id), db: AsyncSession = Depends(get_db)):
    c = await db.get(Coach, coach_id)
    if body.subscribe_enabled is not None:
        c.push_subscribe_enabled = body.subscribe_enabled
    if body.inbox_enabled is not None:
        c.push_inbox_enabled = body.inbox_enabled
    await db.commit()
    return await get_push(coach_id, db)


@router.get("/me/dashboard")
async def dashboard(coach_id: int = Depends(get_current_coach_id), db: AsyncSession = Depends(get_db)) -> dict:
    total = (await db.execute(select(func.count()).select_from(CoachStudent).where(CoachStudent.coach_id == coach_id))).scalar() or 0
    active = (await db.execute(select(func.count()).select_from(CoachStudent).where(
        CoachStudent.coach_id == coach_id, CoachStudent.status == "active"))).scalar() or 0
    uncommented = (await db.execute(select(func.count()).select_from(CheckIn).where(
        CheckIn.coach_id == coach_id, CheckIn.commented == False))).scalar() or 0  # noqa: E712
    # 风险信号（精简）：包月 7 天内到期
    c = await db.get(Coach, coach_id)
    soon = date.today() + timedelta(days=7)
    due = (await db.execute(select(CoachStudent, ).where(
        CoachStudent.coach_id == coach_id, CoachStudent.next_due_date.is_not(None),
        CoachStudent.next_due_date <= soon))).scalars().all()
    signals = [f"包月 7 天内到期：{cs.alias}（{cs.next_due_date}）" for cs in due]
    return {"student_total": total, "active": active, "uncommented": uncommented,
            "risk_signals": signals, "risk_days_threshold": c.risk_days_threshold}


@router.post("/me/invite-codes", status_code=201)
async def create_invite(coach_id: int = Depends(get_current_coach_id), db: AsyncSession = Depends(get_db)) -> dict:
    code = secrets.token_hex(2).upper() + "-" + secrets.token_hex(2).upper()
    ic = InviteCode(code=code, coach_id=coach_id, expires_at=None)
    db.add(ic)
    await db.commit()
    return {"code": code, "expires_in_days": 7, "remaining_uses": 5}
