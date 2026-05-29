"""C-2 列表 / C-3 档案 / 体脂录入。多租户：始终按 coach_id 过滤。"""
from datetime import date as date_t

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_coach_id
from app.db.session import get_db
from app.models import BodyMetric, CheckIn, CoachStudent, Student

router = APIRouter()


class StudentItem(BaseModel):
    id: int
    alias: str
    status: str
    source: str
    tags: list = []
    next_due_date: date_t | None = None
    remaining_sessions: int | None = None
    last_check_in_at: str | None = None


class StudentList(BaseModel):
    items: list[StudentItem]


async def _last_checkin(db: AsyncSession, student_id: int) -> str | None:
    ci = (await db.execute(
        select(CheckIn).where(CheckIn.student_id == student_id).order_by(CheckIn.date.desc()).limit(1)
    )).scalar_one_or_none()
    return ci.date.isoformat() if ci else None


@router.get("/me/students", response_model=StudentList)
async def my_students(coach_id: int = Depends(get_current_coach_id), db: AsyncSession = Depends(get_db)) -> StudentList:
    rows = (await db.execute(
        select(CoachStudent, Student).join(Student, Student.id == CoachStudent.student_id)
        .where(CoachStudent.coach_id == coach_id).order_by(CoachStudent.id)
    )).all()
    items = []
    for cs, s in rows:
        items.append(StudentItem(
            id=s.id, alias=cs.alias or s.display_name or f"学员{s.id}", status=cs.status,
            source=cs.source, tags=cs.tags or [], next_due_date=cs.next_due_date,
            remaining_sessions=cs.remaining_sessions, last_check_in_at=await _last_checkin(db, s.id),
        ))
    return StudentList(items=items)


class StudentDetail(BaseModel):
    id: int
    alias: str
    gender: int | None = None
    birth_year: int | None = None
    height_cm: int | None = None
    goal: str | None = None
    status: str
    source: str
    tags: list = []
    coaching_started_at: date_t | None = None
    next_due_date: date_t | None = None
    remaining_sessions: int | None = None
    lifetime_paid_yuan: int = 0
    current_period_paid_yuan: int = 0
    health_notes: str | None = None
    contraindicated_exercise_ids: list = []


async def _get_cs(db, coach_id, sid) -> tuple[CoachStudent, Student]:
    row = (await db.execute(
        select(CoachStudent, Student).join(Student, Student.id == CoachStudent.student_id)
        .where(CoachStudent.coach_id == coach_id, CoachStudent.student_id == sid)
    )).first()
    if row is None:
        raise HTTPException(404, "student not found under this coach")
    return row[0], row[1]


@router.get("/me/students/{sid}", response_model=StudentDetail)
async def student_detail(sid: int, coach_id: int = Depends(get_current_coach_id), db: AsyncSession = Depends(get_db)):
    cs, s = await _get_cs(db, coach_id, sid)
    return StudentDetail(
        id=s.id, alias=cs.alias or s.display_name or f"学员{s.id}", gender=s.gender,
        birth_year=(s.birth_date.year if s.birth_date else None), height_cm=s.height_cm,
        goal=cs.goal, status=cs.status, source=cs.source, tags=cs.tags or [],
        coaching_started_at=cs.coaching_started_at, next_due_date=cs.next_due_date,
        remaining_sessions=cs.remaining_sessions, lifetime_paid_yuan=cs.lifetime_paid_yuan,
        current_period_paid_yuan=cs.current_period_paid_yuan, health_notes=cs.health_notes,
        contraindicated_exercise_ids=cs.contraindicated_exercise_ids or [],
    )


class StudentUpdate(BaseModel):
    alias: str | None = None
    goal: str | None = None
    status: str | None = None
    next_due_date: date_t | None = None
    remaining_sessions: int | None = None
    health_notes: str | None = None
    ended_reason: str | None = None


@router.put("/me/students/{sid}", response_model=StudentDetail)
async def update_student(sid: int, body: StudentUpdate, coach_id: int = Depends(get_current_coach_id), db: AsyncSession = Depends(get_db)):
    cs, _ = await _get_cs(db, coach_id, sid)
    for k, v in body.model_dump(exclude_unset=True).items():
        setattr(cs, k, v)
    await db.commit()
    return await student_detail(sid, coach_id, db)


class MetricItem(BaseModel):
    date: date_t
    weight_kg: float | None = None
    body_fat_pct: float | None = None
    waist_cm: float | None = None
    chest_cm: float | None = None
    arm_cm: float | None = None


@router.get("/me/students/{sid}/metrics")
async def list_metrics(sid: int, coach_id: int = Depends(get_current_coach_id), db: AsyncSession = Depends(get_db)) -> dict:
    await _get_cs(db, coach_id, sid)
    rows = (await db.execute(select(BodyMetric).where(BodyMetric.student_id == sid).order_by(BodyMetric.date))).scalars().all()
    return {"items": [MetricItem.model_validate(m, from_attributes=True).model_dump(mode="json") for m in rows]}


@router.post("/me/students/{sid}/metrics", status_code=201)
async def add_metric(sid: int, body: MetricItem, coach_id: int = Depends(get_current_coach_id), db: AsyncSession = Depends(get_db)) -> dict:
    await _get_cs(db, coach_id, sid)
    m = BodyMetric(student_id=sid, source="coach", **body.model_dump())
    db.add(m)
    await db.commit()
    return {"ok": True}
