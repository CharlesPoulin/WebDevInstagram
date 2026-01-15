from functools import lru_cache
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings managed by Pydantic.
    Reads from environment variables and .env file.
    """

    # Project Info
    PROJECT_NAME: str = "DefaultPython"
    VERSION: str = "0.1.0"
    DEBUG: bool = False
    ENVIRONMENT: Literal["local", "dev", "prod"] = "local"

    # API Configuration
    API_HOST: str = "127.0.0.1"
    API_PORT: int = 8000

    # Model configuration
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=True
    )


@lru_cache
def get_settings() -> Settings:
    """
    Creates and caches the settings object.
    Usage:
        from defaultpython.config import get_settings
        settings = get_settings()
    """
    return Settings()
