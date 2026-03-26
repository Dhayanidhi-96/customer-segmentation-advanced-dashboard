from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = "customer_segmentation"
    POSTGRES_USER: str = "admin"
    POSTGRES_PASSWORD: str = "admin"
    DATABASE_URL: str | None = None

    REDIS_URL: str = "redis://localhost:6379/0"

    GROK_API_KEY: str = ""
    GROK_MODEL: str = "grok-3-latest"

    SENDGRID_API_KEY: str = ""
    FROM_EMAIL: str = "noreply@example.com"
    FROM_NAME: str = "Customer Segmentation"
    SMTP_HOST: str = "smtp.sendgrid.net"
    SMTP_PORT: int = 587
    SMTP_USERNAME: str = "apikey"
    SMTP_PASSWORD: str = ""

    SECRET_KEY: str = "development-secret"
    FRONTEND_URL: str = "http://localhost:5173"
    BACKEND_URL: str = "http://localhost:8000"
    ENVIRONMENT: str = "development"

    MODEL_RETRAIN_SCHEDULE: str = "0 3 * * 0"
    EMAIL_CAMPAIGN_SCHEDULE: str = "0 2 * * *"
    MLFLOW_TRACKING_URI: str = "./mlruns"

    @property
    def sqlalchemy_database_uri(self) -> str:
        if self.DATABASE_URL:
            return self.DATABASE_URL
        return (
            f"postgresql+psycopg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
