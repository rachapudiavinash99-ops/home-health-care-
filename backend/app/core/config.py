from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "Home Healthcare Management System"
    API_V1_STR: str = "/api/v1"
    
    # Postgres
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "healthcare"
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/healthcare"
    
    # Security
    JWT_SECRET_KEY: str = "DEV_SECRET_KEY"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
