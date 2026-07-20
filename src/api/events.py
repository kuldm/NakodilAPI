from typing import Annotated, List

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Depends, Header

from exceptions import SeatsConflictException, SeatsConflictHTTPException
from schemas.events import EventRead
from schemas.seats import EventSeatRead
from schemas.bookings import BookingCreate
from services.events import EventsService

router = APIRouter(prefix="/events", route_class=DishkaRoute, tags=["Мероприятия"])


def get_current_user_id(x_user_id: Annotated[int, Header()]) -> int:
    return x_user_id


CurrentUserId = Annotated[int, Depends(get_current_user_id)]


@router.get(
    "",
    summary="Получение всех мероприятий",
    description="<h3>Получаем список мероприятий для клиента<h3>",
    response_model=list[EventRead],
)
async def list_events(
    service: FromDishka[EventsService],
):
    events = await service.get_all_events()
    return events


@router.get(
    "/{event_id}",
    summary="Получение мероприятия по ID",
    description="<h3>Получаем данные о мероприятии по его ID<h3>",
    response_model=EventRead,
)
async def get_event(
    event_id: int,
    service: FromDishka[EventsService],
):
    event = await service.get_event_by_id(event_id)
    return event


@router.get(
    "/{event_id}/seats",
    summary="Возвращает места мероприятия",
    description="<h3>Возвращает места на мероприятии с ценами и статусами по ID мероприятия<h3>",
    response_model=List[EventSeatRead],
)
async def list_event_seats(
    event_id: int,
    service: FromDishka[EventsService],
):
    events = await service.get_event_seats(event_id)
    return events


@router.post(
    "/{event_id}/checkout",
    summary="Временно бронирует места",
    description="<h3>Этот метод временно бронирует места за клиентом, возвращает итоговую стоимость и возможность страховки<h3>",
    # response_model=CheckoutResponse,
)
async def prepare_checkout(
    service: FromDishka[EventsService],
    user_id: CurrentUserId,
    event_id: int,
    payload: BookingCreate,
):
    try:
        return await service.prepare_checkout(user_id, event_id, payload)
    except SeatsConflictException:
        raise SeatsConflictHTTPException
