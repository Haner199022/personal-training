"""v1 路由聚合。"""
from fastapi import APIRouter

from app.api.v1 import auth, checkins, coach, exercises, health, plans, students

api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(students.router, prefix="/coaches", tags=["students"])
api_router.include_router(coach.router, tags=["coach"])          # /coaches/me/...
api_router.include_router(exercises.router, tags=["exercises"])  # /exercises, /coaches/me/exercises/...
api_router.include_router(plans.router, tags=["plans"])
api_router.include_router(checkins.router, tags=["checkins"])
