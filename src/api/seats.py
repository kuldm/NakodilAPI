from typing import List

from fastapi import APIRouter

from api.dependencies import DBDep
from schemas.seats import SeatRead, EventSeatReadShort
from services.seats import SeatsService

router = APIRouter(prefix="/seats", tags=["Места"])
router_events_seats = APIRouter(prefix="/events-seats", tags=["Мероприятия и места"])


@router.get(
    "",
    summary="Получение всех мест",
    description="<h3>Получаем список всех мест<h3>",
    response_model=List[SeatRead],
)
async def list_seats(
    db: DBDep,
):
    seats = await SeatsService(db).get_all_seats()
    return seats


@router.post(
    "/filter",
    summary="Получение мест по их id",
    description="<h3>Получаем список мест по переданным ID<h3>",
    response_model=List[SeatRead],
)
async def get_filtered_seats(
    db: DBDep,
    seat_ids: List[int],
):
    seats = await SeatsService(db).get_filtered_seats(seat_ids)
    return seats


@router_events_seats.get(
    "",
    summary="Получение связи мероприятий и мест",
    description="<h3>Получаем список всех связей мероприятий и мест<h3>",
    response_model=List[EventSeatReadShort],
)
async def list_events_seats(
    db: DBDep,
):
    events_seats = await SeatsService(db).get_all_events_seats()
    return events_seats


