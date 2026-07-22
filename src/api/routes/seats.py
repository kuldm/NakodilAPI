from typing import List

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter

# from api.dependencies import DBDep
from schemas.seats import SeatRead, EventSeatReadShort
from services.seats import SeatsService, EventsSeatsService
from infrastructure.postgres.db_manager import DatabaseManager

router = APIRouter(prefix="/seats", route_class=DishkaRoute, tags=["Места"])
router_events_seats = APIRouter(prefix="/events-seats", route_class=DishkaRoute, tags=["Мероприятия и места"])


@router.get(
    "",
    summary="Получение всех мест",
    description="<h3>Получаем список всех мест<h3>",
    response_model=List[SeatRead],
)
async def list_seats(
    db: FromDishka[DatabaseManager],
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
    db: FromDishka[DatabaseManager],
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
    db: FromDishka[DatabaseManager],
):
    events_seats = await EventsSeatsService(db).get_all_events_seats()
    return events_seats


@router_events_seats.get(
    "/{event_id}",
    summary="Получение связи мероприятий и мест пр ID мероприятия",
    description="<h3>Получаем список всех связей мероприятий и мест по ID мероприятия<h3>",
    response_model=List[EventSeatReadShort],
)
async def list_event_seats(
    db: FromDishka[DatabaseManager],
    event_id: int,
):
    events_seats = await EventsSeatsService(db).get_event_seats_by_event_id(event_id)
    return events_seats
