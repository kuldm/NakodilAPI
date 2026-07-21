from typing import List

from schemas.seats import SeatRead, EventSeatReadShort
from services.base import BaseService


class SeatsService(BaseService):
    async def get_all_seats(self) -> list[SeatRead]:
        return await self.db.seats.get_all()

    async def get_filtered_seats(self, ids: List[int]) -> list[SeatRead]:
        if not ids:
            return []
        return await self.db.seats.get_filtered_by_id(ids)


class EventsSeatsService(BaseService):
    async def get_all_events_seats(self) -> list[EventSeatReadShort]:
        return await self.db.events_seats.get_all()

    async def get_event_seats_by_event_id(
        self, event_id: int
    ) -> list[EventSeatReadShort]:
        return await self.db.events_seats.get_event_seats_by_event_id(event_id)
