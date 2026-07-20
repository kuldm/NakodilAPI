from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class PaymentCalculateItemData(BaseModel):
    booking_id: int
    amount: int = Field(description="Cумма брони в копейках")
    currency: str = Field(description="Валюта, например `RUB`")

    model_config = ConfigDict(frozen=True)


class PaymentCalculateData(BaseModel):
    commission: int
    total: int
    payment_methods: list[str]
    expires_at: datetime | None

    model_config = ConfigDict(frozen=True)


class ProtectionCalculateItemData(BaseModel):
    booking_id: int
    ticket_amount: int = Field(description="Стоимость билетов в копейках")
    event_category: str = Field(description="Категория мероприятия")
    event_starts_at: str = Field(description="Дата начала мероприятия в ISO-формате")

    model_config = ConfigDict(frozen=True)


class ProtectionCalculateData(BaseModel):
    available: bool
    price: int
    covered_amount: int
    description: str | None

    model_config = ConfigDict(frozen=True)
