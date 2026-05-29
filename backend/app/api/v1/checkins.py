"""C-1 feed / C-7 打卡详情 + 点评 / 常用语模板。"""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_coach_id
from app.db.session import get_db
from app.models import CheckIn, CoachComment, CoachStudent, Student

router = APIRouter()

# v5 S7 常用语（MVP 先内置一组；coach_comment_template 表后续接）
COMMENT_TEMPLATES = ["重量稳，下次+2.5kg", "核心收紧，注意呼吸节奏", "动作幅度到位，保持", "疲劳偏高，下次降量", "突破！继续"]


@router.get("/coaches/me/check-ins")
async def feed(status: str = "all", source: str = "all", student_id: int | None = None,
               coach_id: int = Depends(get_current_coach_id), db: AsyncSession = Depends(get_db)) -> dict:
    q = (select(CheckIn, CoachStudent, Student)
         .join(CoachStudent, (CoachStudent.student_id == CheckIn.student_id) & (CoachStudent.coach_id == coach_id))
         .join(Student, Student.id == CheckIn.student_id)
         .where(CheckIn.coach_id == coach_id).order_by(CheckIn.date.desc(), CheckIn.id.desc()))
    if status == "uncommented":
        q = q.where(CheckIn.commented == False)  # noqa: E712
    if source != "all":
        q = q.where(CoachStudent.source == source)
    if student_id:
        q = q.where(CheckIn.student_id == student_id)
    rows = (await db.execute(q)).all()
    items = [{
        "id": ci.id, "student_id": ci.student_id,
        "student_name": cs.alias or s.display_name, "source": cs.source,
        "plan_title": ci.plan_title, "date": ci.date.isoformat(),
        "feeling": ci.feeling, "rpe": ci.rpe, "note": ci.note, "commented": ci.commented,
    } for ci, cs, s in rows]
    return {"items": items, "uncommented": sum(1 for x in items if not x["commented"])}


@router.get("/coaches/me/comment-templates")
async def comment_templates(coach_id: int = Depends(get_current_coach_id)) -> dict:
    return {"items": COMMENT_TEMPLATES}


@router.get("/coaches/me/check-ins/{cid}")
async def checkin_detail(cid: int, coach_id: int = Depends(get_current_coach_id), db: AsyncSession = Depends(get_db)) -> dict:
    ci = (await db.execute(select(CheckIn).where(CheckIn.id == cid, CheckIn.coach_id == coach_id))).scalar_one_or_none()
    if ci is None:
        raise HTTPException(404, "check-in not found")
    s = await db.get(Student, ci.student_id)
    comments = (await db.execute(select(CoachComment).where(CoachComment.check_in_id == cid).order_by(CoachComment.id))).scalars().all()
    return {
        "id": ci.id, "student_name": s.display_name, "plan_title": ci.plan_title,
        "date": ci.date.isoformat(), "feeling": ci.feeling, "rpe": ci.rpe, "note": ci.note,
        "sets_detail": ci.sets_detail or [], "commented": ci.commented,
        "comments": [{"text": c.text, "image_urls": c.image_urls} for c in comments],
    }


class CommentIn(BaseModel):
    text: str
    image_urls: list = []


@router.post("/coaches/me/check-ins/{cid}/comment", status_code=201)
async def add_comment(cid: int, body: CommentIn, coach_id: int = Depends(get_current_coach_id), db: AsyncSession = Depends(get_db)) -> dict:
    ci = (await db.execute(select(CheckIn).where(CheckIn.id == cid, CheckIn.coach_id == coach_id))).scalar_one_or_none()
    if ci is None:
        raise HTTPException(404, "check-in not found")
    db.add(CoachComment(check_in_id=cid, coach_id=coach_id, text=body.text, image_urls=body.image_urls))
    ci.commented = True
    await db.commit()
    return {"ok": True}
