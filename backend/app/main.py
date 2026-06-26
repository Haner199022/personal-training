"""FastAPI 应用入口。所有业务路由挂在 /api/v1 下。"""
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import api_router
from app.core.config import get_settings
from app.db.base import Base
from app.db.session import engine
import app.models  # noqa: F401  注册所有表到 Base.metadata

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # dev 便捷：sqlite 自动建表。生产走 alembic，不在此 create_all。
    if settings.database_url.startswith("sqlite"):
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(title="Personal-Training API", version="0.1.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,  # 用 Authorization Bearer，不用 cookie；避免 *+credentials 非法组合
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.api_v1_prefix)


@app.get("/")
async def root() -> dict:
    return {"service": "personal-training", "docs": "/docs", "health": f"{settings.api_v1_prefix}/health"}
