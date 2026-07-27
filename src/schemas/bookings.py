from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field

from infrastructure.postgres.models.models import BookingStatus


class BookingCreate(BaseModel):
    seat_ids: list[int] = Field(min_length=1)


class CheckoutBooking(BaseModel):
    id: int
    event_title: str
    starts_at: datetime
    seats: list[dict[str, Any]]
    base_amount: int
    payment_commission: int
    protection_price: int | None
    with_protection: bool
    reserved_until: datetime


class BookingAdd(BaseModel):
    event_id: int
    user_id: int
    amount: int
    payment_commission: int
    protection_price: int | None = None
    with_protection: bool
    status: BookingStatus = BookingStatus.pending_payment
    reserved_until: datetime


class BookingRead(BaseModel):
    id: int
    event_id: int
    user_id: int
    amount: int
    payment_commission: int
    protection_price: int | None
    with_protection: bool
    status: BookingStatus
    reserved_until: datetime


class BookingPATCH(BaseModel):
    event_id: int | None = None
    user_id: int | None = None
    amount: int | None = None
    payment_commission: int | None = None
    protection_price: int | None = None
    with_protection: bool | None = None
    status: BookingStatus | None = None
    reserved_until: datetime | None = None
