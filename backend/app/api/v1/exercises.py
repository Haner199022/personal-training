"""C-5 动作库（系统预置只读）+ 收藏切换（存 coach.favorite_exercise_ids）。"""
from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_coach_id
from app.db.session import get_db
from app.models import Coach, Exercise

router = APIRouter()


@router.get("/exercises")
async def list_exercises(coach_id: int = Depends(get_current_coach_id), db: AsyncSession = Depends(get_db)) -> dict:
    coach = await db.get(Coach, coach_id)
    favs = set(coach.favorite_exercise_ids or [])
    rows = (await db.execute(select(Exercise).order_by(Exercise.id))).scalars().all()
    return {"items": [{
        "id": e.id, "name": e.name, "category": e.category,
        "target_primary": e.target_primary, "target_secondary": e.target_secondary,
        "demo_video_url": e.demo_video_url, "cues": e.cues,
        "favorite": e.id in favs,
    } for e in rows]}


@router.post("/coaches/me/exercises/{eid}/favorite")
async def toggle_favorite(eid: int, coach_id: int = Depends(get_current_coach_id), db: AsyncSession = Depends(get_db)) -> dict:
    coach = await db.get(Coach, coach_id)
    favs = list(coach.favorite_exercise_ids or [])
    if eid in favs:
        favs.remove(eid)
    else:
        favs.append(eid)
    coach.favorite_exercise_ids = favs
    await db.commit()
    return {"favorite": eid in favs}
