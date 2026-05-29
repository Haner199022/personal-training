"""开发种子数据：教练 + 学员(含 v5 字段) + 动作库 + 体脂 + 计划 + 打卡。
运行：python -m app.seed   （幂等）"""
import asyncio
from datetime import date, timedelta

from sqlalchemy import delete, select

from app.core.security import hash_password
from app.db.base import Base
from app.db.session import SessionLocal, engine
from app.models import (BodyMetric, CheckIn, Coach, CoachComment, CoachStudent,
                        Exercise, Student, TrainingPlan)

DEMO_PHONE, DEMO_PW = "13800138000", "demo1234"

EXERCISES = [
    ("杠铃深蹲", "strength", ["股四头肌", "臀大肌"], ["腘绳肌", "竖脊肌"], "下蹲至大腿与地面平行，重心落足中，膝盖与脚尖同向。"),
    ("罗马尼亚硬拉", "strength", ["腘绳肌", "臀大肌"], ["竖脊肌"], "髋主导后移，背部中立，杠铃贴腿下放至牵拉感。"),
    ("卧推", "strength", ["胸大肌", "肱三头肌"], ["三角肌前束"], "肩胛后缩下沉，杠铃落于乳线，全程稳定。"),
    ("引体向上", "strength", ["背阔肌", "肱二头肌"], ["斜方肌中下部"], "肩胛先下沉再上拉，下巴过杠，控制离心。"),
    ("过头推举", "strength", ["三角肌", "肱三头肌"], ["上斜方肌"], "核心收紧不塌腰，杠铃走直线过头。"),
    ("硬拉", "strength", ["臀大肌", "竖脊肌"], ["腘绳肌", "斜方肌"], "起杠贴胫骨，髋膝同步伸展，顶峰锁定。"),
    ("壶铃摇摆", "strength", ["臀大肌", "腘绳肌"], ["核心"], "髋部铰链发力，非手臂上举，呼吸配合髋伸。"),
    ("农夫行走", "strength", ["前臂", "斜方肌"], ["核心"], "挺胸收腹，步幅稳定，握距与肩同宽。"),
    ("波比跳", "cardio", ["全身"], [], "下蹲—撑地—跳起一气呵成，落地缓冲。"),
    ("划船机", "cardio", ["背阔肌", "股四头肌"], ["核心"], "腿—髋—臂顺序发力，回程相反顺序。"),
    ("平板支撑", "mobility", ["核心"], ["三角肌前束"], "肘肩同宽，身体一条直线，不塌腰不抬臀。"),
    ("臀桥", "mobility", ["臀大肌"], ["腘绳肌"], "顶峰夹臀，下背不过度伸展。"),
]

STUDENTS = [
    # name, status, source, tags, due_in_days, sessions, health, contra
    ("林楠", "active", "private", [{"name": "增肌", "color": "cyan"}], 30, 8, "右膝半月板术后 2024-08，恢复良好", [1]),
    ("陈一鸣", "active", "gym_assigned", [{"name": "孕产", "color": "green"}], None, 12, None, []),
    ("王雪", "trial", "referral", [{"name": "赛前", "color": "yellow"}], 6, 2, None, []),
    ("赵航", "pending_renewal", "private", [{"name": "增肌", "color": "cyan"}], 2, 1, "腰椎间盘突出 L4-L5", [6]),
    ("周敏", "paused", "gym_assigned", [], None, None, None, []),
    ("孙磊", "churned", "private", [], None, None, None, []),
]


async def main() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with SessionLocal() as db:
        # exercises (idempotent)
        if not (await db.execute(select(Exercise).limit(1))).first():
            for name, cat, prim, sec, cues in EXERCISES:
                db.add(Exercise(name=name, category=cat, target_primary=prim, target_secondary=sec, cues=cues))
            await db.flush()

        coach = (await db.execute(select(Coach).where(Coach.phone == DEMO_PHONE))).scalar_one_or_none()
        if coach is None:
            coach = Coach(phone=DEMO_PHONE, password_hash=hash_password(DEMO_PW), display_name="张教练",
                          bio="10 年力量训练经验，专注体能与赛事备赛。", cert_tags=["NSCA-CPT", "Hyrox L1"],
                          affiliated_studio="乐刻五道口店", subscription_tier="pro_99",
                          profile_intro_rich="带过 200+ 学员，擅长增肌减脂与 Hyrox 备赛。", profile_published=True)
            db.add(coach)
            await db.flush()

        if (await db.execute(select(CoachStudent).where(CoachStudent.coach_id == coach.id))).first():
            print("already seeded relations; skip"); await db.commit(); return

        today = date.today()
        for i, (name, status, source, tags, due, sess, health, contra) in enumerate(STUDENTS, 1):
            stu = Student(wx_openid=f"demo_openid_{i}", display_name=name,
                          gender=1 if i % 2 else 2, height_cm=170 + i, birth_date=date(1995, 1, 1))
            db.add(stu); await db.flush()
            db.add(CoachStudent(
                coach_id=coach.id, student_id=stu.id, alias=name, status=status, source=source, tags=tags,
                goal="增肌减脂，三个月体脂 18%→14%" if i == 1 else "保持体能",
                coaching_started_at=today - timedelta(days=40),
                next_due_date=(today + timedelta(days=due)) if due is not None else None,
                remaining_sessions=sess, lifetime_paid_yuan=4000 * i, current_period_paid_yuan=4000,
                health_notes=health, contraindicated_exercise_ids=contra,
            ))
            # 体脂曲线（前两个学员）
            if i <= 2:
                for w in range(6):
                    db.add(BodyMetric(student_id=stu.id, date=today - timedelta(days=(5 - w) * 14),
                                      weight_kg=78 - w * 0.5, body_fat_pct=22.1 - w * 0.34,
                                      waist_cm=82 - w * 0.8, chest_cm=100 + w * 0.4, arm_cm=35 + w * 0.2, source="coach"))
            # 打卡（前三个学员，部分未点评）
            if i <= 3:
                sets = [{"exercise": "杠铃深蹲", "prescribed": "4×8-10 @60kg",
                         "actual": ["10@60", "10@60", "8@60", "6@55⚠"]},
                        {"exercise": "罗马尼亚硬拉", "prescribed": "4×10 @70kg", "actual": ["10@70"] * 4}]
                db.add(CheckIn(student_id=stu.id, coach_id=coach.id, plan_title="5月增肌周期 W3",
                               date=today - timedelta(days=i), feeling=5 - i, rpe=6 + i,
                               note=["深蹲掉重了5kg", "卧推突破PR 80kg×5", "太累了"][i - 1],
                               sets_detail=sets, commented=(i == 2)))
            # 一个示例计划
            if i == 1:
                db.add(TrainingPlan(coach_id=coach.id, student_id=stu.id, title="5月增肌周期 W3",
                                    goal="本周突破深蹲 PR", status="active", start_date=today,
                                    detail={"sessions": [{"day": "周一", "title": "下肢力量 A", "exercises": [
                                        {"name": "杠铃深蹲", "sets": 4, "reps": "8-10", "weight": "60kg", "primary": "股四头肌·臀大肌"},
                                        {"name": "罗马尼亚硬拉", "sets": 4, "reps": "10", "weight": "70kg", "primary": "腘绳肌·臀大肌"}]}]}))

        # 一个训练模板
        db.add(TrainingPlan(coach_id=coach.id, student_id=None, title="减脂期 W1-W4（4周）",
                            goal="体脂下降导向", status="template", is_template=True,
                            detail={"sessions": [{"day": "周一", "title": "全身循环", "exercises": [
                                {"name": "壶铃摇摆", "sets": 5, "reps": "20", "weight": "16kg", "primary": "臀大肌·腘绳肌"}]}]}))

        await db.commit()
        print(f"✅ seeded: coach({DEMO_PHONE}/{DEMO_PW}) + {len(STUDENTS)} students + {len(EXERCISES)} exercises + metrics/plans/check-ins")


if __name__ == "__main__":
    asyncio.run(main())
