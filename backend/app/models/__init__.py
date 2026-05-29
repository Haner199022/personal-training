"""模型聚合。MVP 骨架先建 4 张核心表；其余按 vault _shared/data-model.md v5
（共 16 张）逐步用 alembic migration 补齐。"""
from app.models.coach import Coach
from app.models.student import Student
from app.models.coach_student import CoachStudent
from app.models.invite_code import InviteCode

__all__ = ["Coach", "Student", "CoachStudent", "InviteCode"]
