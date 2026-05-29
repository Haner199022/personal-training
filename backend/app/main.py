"""FastAPI 应用入口。所有业务路由挂在 /api/v1 下。"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import api_router
from app.core.config import get_settings

settings = get_settings()

app = FastAPI(title="Personal-Training API", version="0.1.0")

# 教练端 Web 走 COS/CDN 跨域访问 API；MVP 先放开，上线收紧白名单。
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.api_v1_prefix)


@app.get("/")
async def root() -> dict:
    return {"service": "personal-training", "docs": "/docs", "health": f"{settings.api_v1_prefix}/health"}
