"""异步引擎 + session 依赖。

多租户提醒：业务查询必须显式带 coach_id 过滤；Phase 2 上 PG RLS 时
在此处的 session 上 `SET app.current_coach_id = ?`（PgBouncer 必须 session pooling）。
"""
from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import get_settings

_settings = get_settings()
engine = create_async_engine(_settings.database_url, pool_pre_ping=True, future=True)
SessionLocal = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session
