from typing import Literal
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    MODE: Literal["TEST", "LOCAL", "DEV", "PROD"]

    API_URL: str

    APP_NAME: str
    DEVELOPER: str

    DATABASE_URL: str
    PAYMENT_API_URL: str
    PROTECTION_API_URL: str
    BOOKING_TTL_MINUTES: int

    RESERVATION_MINUTES: int

    PAYMENT_TIMEOUT: float
    PROTECTION_TIMEOUT: float

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


settings = Settings()  # type: ignore[call-arg]
