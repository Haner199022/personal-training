"""模型聚合（v5 子集：核心关系 + 动作/体脂/计划/打卡）。完整 16+ 表见 data-model.md。"""
from app.models.coach import Coach
from app.models.student import Student
from app.models.coach_student import CoachStudent
from app.models.invite_code import InviteCode
from app.models.exercise import Exercise
from app.models.body_metric import BodyMetric
from app.models.training_plan import TrainingPlan
from app.models.check_in import CheckIn, CoachComment

__all__ = ["Coach", "Student", "CoachStudent", "InviteCode", "Exercise",
           "BodyMetric", "TrainingPlan", "CheckIn", "CoachComment"]
