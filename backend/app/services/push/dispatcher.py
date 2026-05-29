"""入口：按事件类型路由到 Tier 1/2/3。每个事件至少落 Tier3 站内信。"""
from enum import StrEnum


class PushEvent(StrEnum):
    REMIND_PUNCH = "remind_punch"        # 18:00 未打卡催促
    COMMENT_PUBLISHED = "comment_published"
    BODY_WEEKLY = "body_weekly"
    SIGNUP_OK = "signup_ok"
    BROADCAST = "broadcast"


async def dispatch(coach_id: int, student_id: int, event: PushEvent, payload: dict) -> None:
    """路由占位。真实实现：
    1) 始终 await tier3_inbox.write(...)
    2) 按路由表 enqueue tier1（群机器人，按 coach_id 分桶限流）
    3) 命中 tier2 场景且学员有授权次数 → 发订阅消息
    """
    raise NotImplementedError
