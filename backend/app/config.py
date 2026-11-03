from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class Settings(BaseSettings):
    """KrishiSathi Application Configuration Settings"""

    # Project metadata
    PROJECT_NAME: str = "KrishiSathi"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "AI-Powered Multi-Agent Agricultural Climate Intelligence"

    # AWS & Bedrock
    AWS_REGION: str = "us-east-1"
    AWS_DEFAULT_REGION: str = "us-east-1"
    BEDROCK_MODEL_ID: str = "anthropic.claude-3-5-sonnet-20241022-v2:0"

    # Weather APIs
    OPEN_METEO_BASE_URL: str = "https://api.open-meteo.com/v1/forecast"
    OPEN_METEO_GEO_URL: str = "https://geocoding-api.open-meteo.com/v1/search"
    IMD_WEATHER_URL: str = "https://mausam.imd.gov.in"

    # Database
    DATABASE_URL: str = "sqlite:///./krishisathi.db"

    # Networking & CORS
    BACKEND_HOST: str = "0.0.0.0"
    BACKEND_PORT: int = 8000
    FRONTEND_URL: str = "http://localhost:5173"
    ALLOWED_ORIGINS: list[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "https://krishisathi.vercel.app",
    ]

    # Environment
    ENVIRONMENT: str = "development"
    LOG_LEVEL: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()

