from pydantic_settings import BaseSettings
from functools import lru_cache
from pathlib import Path


class Settings(BaseSettings):
    APP_NAME: str = "Trupy AI"
    APP_VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"

    LLM_API_KEY: str = "your-api-key"
    BASE_URL: str | None = "your-base-url"
    MODEL: str = "your-model"

    DATABASE_URL: str = "sqlite+aiosqlite:///./trupy.db"

    REDIS_URL: str = "redis://localhost:6379/0"
    
    SESSION_TTL: int = 900

    RATE_LIMIT_CHAT: str = "30/minute"

    LOGS_DIR: Path = Path("app/logs")

    CORS_ORIGINS: list[str] = ["*"]

    class Config:
        env_file = ".env"
        extra = "ignore"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
