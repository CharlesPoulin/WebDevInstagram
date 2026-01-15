from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://user:pass@localhost:5432/ugram"
    SECRET_KEY: str = "secret"


settings = Settings()
