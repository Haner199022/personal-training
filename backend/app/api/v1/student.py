"""学员端 API（/students/me/...）。学员可跟多教练，这里取「主教练」= 最近加入的 active 关系。"""
from datetime import date as date_t

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_student_id
from app.db.session import get_db
from app.models import (BodyMetric, CheckIn, Coach, CoachComment, CoachStudent,
                        InviteCode, Student, TrainingPlan)

router = APIRouter(prefix="/students")


async def _primary_cs(db: AsyncSession, sid: int) -> CoachStudent | None:
    return (await db.execute(
        select(CoachStudent).where(CoachStudent.student_id == sid).order_by(CoachStudent.id.desc()).limit(1)
    )).scalar_one_or_none()


@router.get("/me")
async def me(sid: int = Depends(get_current_student_id), db: AsyncSession = Depends(get_db)) -> dict:
    s = await db.get(Student, sid)
    cs = await _primary_cs(db, sid)
    coach = await db.get(Coach, cs.coach_id) if cs else None
    return {
        "id": s.id, "display_name": s.display_name or "学员",
        "bound": cs is not None,
        "coach": {"id": coach.id, "name": coach.display_name} if coach else None,
    }


@router.get("/me/today")
async def today(sid: int = Depends(get_current_student_id), db: AsyncSession = Depends(get_db)) -> dict:
    cs = await _primary_cs(db, sid)
    if cs is None:
        return {"bound": False}
    plan = (await db.execute(select(TrainingPlan).where(
        TrainingPlan.student_id == sid, TrainingPlan.status == "active"
    ).order_by(TrainingPlan.id.desc()).limit(1))).scalar_one_or_none()
    if plan is None:
        return {"bound": True, "rest": True}
    sessions = (plan.detail or {}).get("sessions", [])
    sess = sessions[0] if sessions else None
    return {"bound": True, "rest": sess is None, "plan_id": plan.id, "plan_title": plan.title,
            "session": sess, "exercise_count": len(sess["exercises"]) if sess else 0}


class JoinIn(BaseModel):
    invite_code: str


@router.post("/me/join")
async def join(body: JoinIn, sid: int = Depends(get_current_student_id), db: AsyncSession = Depends(get_db)) -> dict:
    ic = (await db.execute(select(InviteCode).where(InviteCode.code == body.invite_code.strip().upper()))).scalar_one_or_none()
    if ic is None:
        raise HTTPException(404, "邀请码无效")
    exists = (await db.execute(select(CoachStudent).where(
        CoachStudent.coach_id == ic.coach_id, CoachStudent.student_id == sid))).scalar_one_or_none()
    if exists is None:
        db.add(CoachStudent(coach_id=ic.coach_id, student_id=sid, status="active", source="referral"))
        ic.used_count = (ic.used_count or 0) + 1
        await db.commit()
    coach = await db.get(Coach, ic.coach_id)
    return {"ok": True, "coach_name": coach.display_name}


@router.get("/me/plan")
async def my_plan(sid: int = Depends(get_current_student_id), db: AsyncSession = Depends(get_db)) -> dict:
    plan = (await db.execute(select(TrainingPlan).where(
        TrainingPlan.student_id == sid, TrainingPlan.status == "active"
    ).order_by(TrainingPlan.id.desc()).limit(1))).scalar_one_or_none()
    if plan is None:
        return {"plan": None}
    return {"plan": {"id": plan.id, "title": plan.title, "goal": plan.goal, "detail": plan.detail or {}}}


class CheckInIn(BaseModel):
    plan_title: str
    feeling: int | None = None
    rpe: int | None = None
    note: str | None = None
    sets_detail: list = []


@router.post("/me/check-ins", status_code=201)
async def submit_checkin(body: CheckInIn, sid: int = Depends(get_current_student_id), db: AsyncSession = Depends(get_db)) -> dict:
    cs = await _primary_cs(db, sid)
    if cs is None:
        raise HTTPException(400, "未绑定教练")
    ci = CheckIn(student_id=sid, coach_id=cs.coach_id, plan_title=body.plan_title, date=date_t.today(),
                 feeling=body.feeling, rpe=body.rpe, note=body.note, sets_detail=body.sets_detail, commented=False)
    db.add(ci)
    await db.commit()
    await db.refresh(ci)
    return {"id": ci.id}


@router.get("/me/check-ins")
async def my_checkins(sid: int = Depends(get_current_student_id), db: AsyncSession = Depends(get_db)) -> dict:
    rows = (await db.execute(select(CheckIn).where(CheckIn.student_id == sid).order_by(CheckIn.date.desc()))).scalars().all()
    return {"items": [{"id": c.id, "plan_title": c.plan_title, "date": c.date.isoformat(),
                       "feeling": c.feeling, "rpe": c.rpe, "commented": c.commented} for c in rows]}


@router.get("/me/check-ins/{cid}")
async def checkin_result(cid: int, sid: int = Depends(get_current_student_id), db: AsyncSession = Depends(get_db)) -> dict:
    ci = (await db.execute(select(CheckIn).where(CheckIn.id == cid, CheckIn.student_id == sid))).scalar_one_or_none()
    if ci is None:
        raise HTTPException(404, "not found")
    comments = (await db.execute(select(CoachComment, Coach).join(Coach, Coach.id == CoachComment.coach_id)
                .where(CoachComment.check_in_id == cid).order_by(CoachComment.id))).all()
    return {"id": ci.id, "plan_title": ci.plan_title, "date": ci.date.isoformat(),
            "comments": [{"text": c.text, "image_urls": c.image_urls, "coach_name": co.display_name} for c, co in comments]}


class MetricIn(BaseModel):
    date: date_t
    weight_kg: float | None = None
    body_fat_pct: float | None = None
    waist_cm: float | None = None
    chest_cm: float | None = None
    arm_cm: float | None = None
    note: str | None = None


@router.get("/me/metrics")
async def my_metrics(sid: int = Depends(get_current_student_id), db: AsyncSession = Depends(get_db)) -> dict:
    rows = (await db.execute(select(BodyMetric).where(BodyMetric.student_id == sid).order_by(BodyMetric.date))).scalars().all()
    return {"items": [{"date": m.date.isoformat(), "weight_kg": m.weight_kg, "body_fat_pct": m.body_fat_pct,
                       "waist_cm": m.waist_cm, "chest_cm": m.chest_cm, "arm_cm": m.arm_cm} for m in rows]}


@router.post("/me/metrics", status_code=201)
async def add_my_metric(body: MetricIn, sid: int = Depends(get_current_student_id), db: AsyncSession = Depends(get_db)) -> dict:
    db.add(BodyMetric(student_id=sid, source="student", **body.model_dump()))
    await db.commit()
    return {"ok": True}


@router.get("/me/coach")
async def my_coach(sid: int = Depends(get_current_student_id), db: AsyncSession = Depends(get_db)) -> dict:
    cs = await _primary_cs(db, sid)
    if cs is None:
        return {"coach": None}
    c = await db.get(Coach, cs.coach_id)
    return {"coach": {"name": c.display_name, "bio": c.bio, "cert_tags": c.cert_tags or [],
                      "intro": c.profile_intro_rich if c.profile_published else None,
                      "studio": c.affiliated_studio}}


@router.get("/me/inbox")
async def inbox(sid: int = Depends(get_current_student_id), db: AsyncSession = Depends(get_db)) -> dict:
    """Tier 3 站内信。MVP 从教练点评派生（点评通知）+ 一条提醒占位。
    完整 student_inbox 表见 data-model.md，后续接入。"""
    rows = (await db.execute(select(CheckIn).where(CheckIn.student_id == sid, CheckIn.commented == True)  # noqa: E712
            .order_by(CheckIn.date.desc()))).scalars().all()
    items = [{"id": f"comment-{c.id}", "title": "教练点评了你的打卡", "sub": f"{c.plan_title} · {c.date.isoformat()}",
              "read": False, "link": f"/pages/checkin-result/checkin-result?id={c.id}"} for c in rows]
    items.append({"id": "remind-0", "title": "记得今天 18:00 前打卡", "sub": "今天 09:00", "read": True, "link": ""})
    return {"items": items, "unread": sum(1 for x in items if not x["read"])}
