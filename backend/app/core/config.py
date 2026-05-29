"""集中配置：pydantic-settings 从 .env 读，缺关键项 fail-fast。"""
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_env: str = "dev"
    api_v1_prefix: str = "/api/v1"

    database_url: str = "postgresql+psycopg://app_user:pwd@localhost:5432/personal_training"
    redis_url: str = "redis://localhost:6379/0"

    jwt_secret: str = "dev-only-change-me"
    jwt_alg: str = "HS256"
    jwt_expire_minutes: int = 60 * 24 * 7

    wx_app_id: str = ""
    wx_app_secret: str = ""

    # 缺失则 push 服务 Tier1 加密会 fail-fast（见 services/push）
    webhook_encrypt_key: str = ""

    cos_region: str = "ap-shanghai"
    cos_bucket: str = ""
    cos_secret_id: str = ""
    cos_secret_key: str = ""

    sentry_dsn: str = ""


@lru_cache
def get_settings() -> Settings:
    return Settings()
