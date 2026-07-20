from datetime import datetime

from pydantic import BaseModel

from models.models import SeatStatus


class SeatRead(BaseModel):
    id: int
    location_id: int
    sector: str
    row: int
    number: int
    x: int
    y: int


class EventSeatRead(BaseModel):
    id: int
    event_id: int
    seat_id: int
    sector: str
    row: int
    number: int
    x: int
    y: int
    price: int
    status: SeatStatus
    reserved_until: datetime | None
    booking_id: int | None


class EventSeatReadShort(BaseModel):
    id: int
    event_id: int
    seat_id: int
    price: int
    status: SeatStatus
    reserved_until: datetime | None
    booking_id: int | None

