from typing import List

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter

from api.routes.events import CurrentUserId
from schemas.events import (
    EventCreate,
    EventRead,
)
from schemas.schemas import EventDashboard
from services.organizers import OrganizersService

router = APIRouter(prefix="/organizer", route_class=DishkaRoute, tags=["Организатор"])


@router.get(
    "/events",
    summary="Получение событий организатора",
    description="<h3>Этот метод возвращает список созданных событий текущего организатора<h3>",
    response_model=List[EventRead],
)
async def list_organizer_events(
    organizer_id: CurrentUserId,
    service: FromDishka[OrganizersService],
):
    return await service.get_organizer_events(organizer_id)


@router.post(
    "/events",
    summary="Создает мероприятие",
    description="<h3>Создает мероприятие от лица текущего организатора<h3>",
    response_model=EventRead,
)
async def create_event(
    payload: EventCreate,
    organizer_id: CurrentUserId,
    service: FromDishka[OrganizersService],
):
    return await service.create_organizer_event(organizer_id, payload)


@router.get(
    "/events/{event_id}/dashboard",
    summary="Возвращает аналитику по мероприятию",
    description="<h3>Возвращает аналитические данные для дашборда по мероприятию<h3>",
    response_model=EventDashboard,
)
async def get_event_dashboard(
    event_id: int,
    organizer_id: CurrentUserId,
    service: FromDishka[OrganizersService],
):
    return await service.get_event_dashboard(event_id, organizer_id)
