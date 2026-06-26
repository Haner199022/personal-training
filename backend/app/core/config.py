"""集中配置：pydantic-settings 从 .env 读，非 dev 环境对弱密钥 fail-fast。"""
from functools import lru_cache

from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_env: str = "dev"
    api_v1_prefix: str = "/api/v1"

    database_url: str = "sqlite+aiosqlite:///./dev.db"  # dev 默认；生产在 .env 设 postgresql+psycopg://...
    redis_url: str = "redis://localhost:6379/0"

    jwt_secret: str = "dev-only-change-me"
    jwt_alg: str = "HS256"
    jwt_expire_minutes: int = 60 * 24 * 7

    wx_app_id: str = ""
    wx_app_secret: str = ""
    webhook_encrypt_key: str = ""

    cos_region: str = "ap-shanghai"
    cos_bucket: str = ""
    cos_secret_id: str = ""
    cos_secret_key: str = ""
    sentry_dsn: str = ""

    @model_validator(mode="after")
    def _guard_non_dev(self) -> "Settings":
        # dev 允许占位；任何非 dev 环境必须显式提供强密钥 + 非 sqlite，否则启动即失败
        if self.app_env != "dev":
            if self.jwt_secret in ("", "dev-only-change-me"):
                raise ValueError("JWT_SECRET 必须在非 dev 环境设为强随机值（不能用默认占位）")
            if self.database_url.startswith("sqlite"):
                raise ValueError("SQLite 仅限 dev；非 dev 请设 postgresql+psycopg:// 的 DATABASE_URL")
        return self


@lru_cache
def get_settings() -> Settings:
    return Settings()
