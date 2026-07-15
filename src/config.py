from typing import Literal
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    MODE: Literal["TEST", "LOCAL", "DEV", "PROD"]

    API_URL: str

    APP_NAME: str
    DEVELOPER: str

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings() # type: ignore[call-arg]
