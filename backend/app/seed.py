"""开发种子数据：1 个演示教练 + 若干学员 + 关系。
运行：python -m app.seed   （幂等：已存在则跳过）"""
import asyncio

from sqlalchemy import select

from app.core.security import hash_password
from app.db.base import Base
from app.db.session import SessionLocal, engine
from app.models import Coach, CoachStudent, Student

DEMO_PHONE = "13800138000"
DEMO_PW = "demo1234"

_STUDENTS = [
    ("林楠", "active"),
    ("陈一鸣", "active"),
    ("王雪", "trial"),
    ("赵航", "pending_renewal"),
    ("周敏", "paused"),
    ("孙磊", "churned"),
]


async def main() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with SessionLocal() as db:
        coach = (await db.execute(select(Coach).where(Coach.phone == DEMO_PHONE))).scalar_one_or_none()
        if coach is None:
            coach = Coach(
                phone=DEMO_PHONE,
                password_hash=hash_password(DEMO_PW),
                display_name="张教练",
                bio="NSCA-CPT · Hyrox L1 · 自由私教",
                subscription_tier="pro_99",
            )
            db.add(coach)
            await db.flush()

        existing = (
            await db.execute(select(CoachStudent).where(CoachStudent.coach_id == coach.id))
        ).scalars().all()
        if not existing:
            for i, (name, status) in enumerate(_STUDENTS, start=1):
                stu = Student(wx_openid=f"demo_openid_{i}", display_name=name)
                db.add(stu)
                await db.flush()
                db.add(CoachStudent(coach_id=coach.id, student_id=stu.id, alias=name, status=status))

        await db.commit()
        print(f"✅ seeded: coach id={coach.id} ({DEMO_PHONE}/{DEMO_PW}), students={len(_STUDENTS)}")


if __name__ == "__main__":
    asyncio.run(main())
