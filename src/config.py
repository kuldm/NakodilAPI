from typing import Literal

from pydantic import BaseModel, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class ReportConfig(BaseModel):
    api_url: str


class BookingConfig(BaseModel):
    reservation_minutes: int


class AppConfig(BaseModel):
    app_name: str
    developer: str
    mode: Literal["TEST", "LOCAL", "DEV", "PROD"]


class PaymentApiConfig(BaseModel):
    base_url: str
    timeout: float = 5.0


class ProtectionApiConfig(BaseModel):
    base_url: str
    timeout: float = 5.0


class ConnectorsConfig(BaseModel):
    payment: PaymentApiConfig
    protection: ProtectionApiConfig


class PostgresConfig(BaseModel):
    host: str
    port: int
    user: str
    password: SecretStr
    database: str

    echo: bool = False
    pool_size: int = 10
    max_overflow: int = 20

    @property
    def url(self) -> str:
        return (
            f"postgresql+psycopg://{self.user}:"
            f"{self.password.get_secret_value()}"
            f"@{self.host}:{self.port}/{self.database}"
        )


class Settings(BaseSettings):
    app: AppConfig
    postgres: PostgresConfig
    booking: BookingConfig
    report: ReportConfig
    connectors: ConnectorsConfig

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
        extra="ignore",
    )


settings = Settings()
