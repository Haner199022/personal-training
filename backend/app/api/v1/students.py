"""C-2 学员列表。多租户：永远按 current coach_id 过滤。"""
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_coach_id
from app.db.session import get_db
from app.models import CoachStudent, Student

router = APIRouter()


class StudentItem(BaseModel):
    id: int
    alias: str
    status: str
    last_check_in_at: str | None = None


class StudentList(BaseModel):
    items: list[StudentItem]


@router.get("/me/students", response_model=StudentList)
async def my_students(
    coach_id: int = Depends(get_current_coach_id),
    db: AsyncSession = Depends(get_db),
) -> StudentList:
    rows = (
        await db.execute(
            select(CoachStudent, Student)
            .join(Student, Student.id == CoachStudent.student_id)
            .where(CoachStudent.coach_id == coach_id)  # 行级隔离习惯
            .order_by(CoachStudent.id)
        )
    ).all()
    items = [
        StudentItem(
            id=s.id,
            alias=cs.alias or s.display_name or f"学员{s.id}",
            status=cs.status,
            last_check_in_at=None,  # 待 check_in 表接入
        )
        for cs, s in rows
    ]
    return StudentList(items=items)
