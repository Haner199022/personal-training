"""推送 worker：每个 coach_id 一条消费协程，令牌桶限流 + 指数退避(1s/4s/16s)，
3 次失败写 push_dead_letter + Sentry。MVP 可作为 FastAPI BackgroundTask 跑，
Phase 2 独立进程：python -m app.workers.push"""


async def run() -> None:
    raise NotImplementedError
