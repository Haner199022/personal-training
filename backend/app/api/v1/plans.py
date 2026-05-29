"""C-4 训练计划：列表 / 新建 / 模板库。detail 树用 JSON。"""
from datetime import date as date_t

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_coach_id
from app.db.session import get_db
from app.models import TrainingPlan

router = APIRouter()


def _dump(p: TrainingPlan) -> dict:
    return {"id": p.id, "title": p.title, "goal": p.goal, "status": p.status,
            "is_template": p.is_template, "student_id": p.student_id,
            "start_date": p.start_date.isoformat() if p.start_date else None,
            "detail": p.detail or {}}


@router.get("/coaches/me/students/{sid}/plans")
async def student_plans(sid: int, coach_id: int = Depends(get_current_coach_id), db: AsyncSession = Depends(get_db)) -> dict:
    rows = (await db.execute(select(TrainingPlan).where(
        TrainingPlan.coach_id == coach_id, TrainingPlan.student_id == sid
    ).order_by(TrainingPlan.id.desc()))).scalars().all()
    return {"items": [_dump(p) for p in rows]}


@router.get("/coaches/me/plan-templates")
async def plan_templates(coach_id: int = Depends(get_current_coach_id), db: AsyncSession = Depends(get_db)) -> dict:
    rows = (await db.execute(select(TrainingPlan).where(
        TrainingPlan.coach_id == coach_id, TrainingPlan.is_template == True  # noqa: E712
    ).order_by(TrainingPlan.id.desc()))).scalars().all()
    return {"items": [_dump(p) for p in rows]}


class PlanIn(BaseModel):
    title: str
    goal: str | None = None
    student_id: int | None = None
    start_date: date_t | None = None
    is_template: bool = False
    detail: dict = {}


@router.post("/coaches/me/plans", status_code=201)
async def create_plan(body: PlanIn, coach_id: int = Depends(get_current_coach_id), db: AsyncSession = Depends(get_db)) -> dict:
    p = TrainingPlan(coach_id=coach_id, status="template" if body.is_template else "draft", **body.model_dump())
    db.add(p)
    await db.commit()
    return _dump(p)
