from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    app_name: str = "System Health Check API"
    app_version: str = "1.0.0"
    host: str = "0.0.0.0"
    port: int = 8080
    log_level: str = "INFO"
    request_timeout: int = 5


@lru_cache
def get_settings() -> Settings:
    """Return cached application settings."""
    return Settings()
