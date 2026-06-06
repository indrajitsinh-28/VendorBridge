from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


BACKEND_ROOT = Path(__file__).resolve().parents[1]
WORKSPACE_ROOT = BACKEND_ROOT.parent


class Settings(BaseSettings):
    database_url: str = Field(default="postgresql+asyncpg://user:password@localhost/vendorbridge", alias="DATABASE_URL")
    secret_key: str = Field(default="change-me-in-env", alias="SECRET_KEY")
    algorithm: str = Field(default="HS256", alias="JWT_ALGORITHM")
    access_token_expire_minutes: int = Field(default=60, alias="ACCESS_TOKEN_EXPIRE_MINUTES")
    smtp_host: str = Field(default="smtp.gmail.com", alias="SMTP_HOST")
    smtp_port: int = Field(default=587, alias="SMTP_PORT")
    smtp_user: str = Field(default="your@gmail.com", alias="SMTP_USER")
    smtp_password: str = Field(default="your_app_password", alias="SMTP_PASSWORD")
    sql_echo: bool = Field(default=False, alias="SQL_ECHO")

    model_config = SettingsConfigDict(
        env_file=(WORKSPACE_ROOT / ".env", BACKEND_ROOT / ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
