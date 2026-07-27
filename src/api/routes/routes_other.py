from typing import Annotated

from fastapi import APIRouter, Depends, Header

from schemas.schemas import (
    LocationDetail,
    LocationRead,
    PaymentCompleted,
    PaymentCreate,
    SeatRead,
)

router = APIRouter()


def get_current_user_id(x_user_id: Annotated[int, Header()]) -> int:
    return x_user_id


CurrentUserId = Annotated[int, Depends(get_current_user_id)]


@router.get("/locations")
async def list_locations() -> list[LocationRead]:
    """Возвращает список площадок."""
    ...


@router.get("/locations/{location_id}")
async def get_location(location_id: int) -> LocationDetail:
    """Возвращает площадку со схемой мест."""
    ...


@router.get("/locations/{location_id}/seats")
async def list_location_seats(location_id: int) -> list[SeatRead]:
    """Возвращает все места площадки."""
    ...


@router.post("/bookings/{booking_id}/pay")
async def pay_booking(
    booking_id: int,
    payload: PaymentCreate,
    user_id: CurrentUserId,
) -> PaymentCompleted:
    """Принимает способ оплаты и флаг with_protection."""
    ...
