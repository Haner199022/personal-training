"""按 coach_id 分桶的令牌桶：群机器人 webhook 20 msg/min/桶（硬上限，超限返回 45009 丢消息）。
MVP 单机用 aiolimiter；Phase 2 换 Redis 分布式令牌桶。"""


class CoachTokenBucket:
    rate = 20 / 60.0  # 20 msg / 60s
    capacity = 20

    async def acquire(self, coach_id: int) -> None:
        # TODO: aiolimiter.AsyncLimiter(20, 60) per coach_id，或 Redis INCR+EXPIRE
        raise NotImplementedError
