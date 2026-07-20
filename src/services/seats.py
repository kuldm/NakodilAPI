from typing import List

from schemas.seats import SeatRead, EventSeatRead, EventSeatReadShort
from services.base import BaseService


class SeatsService(BaseService):
    async def get_all_seats(self) -> SeatRead:
        return await self.db.seats.get_all()

    async def get_filtered_seats(self, ids: List[int]) -> SeatRead:
        if not ids:
            return []
        return await self.db.seats.get_filtered_by_id(ids)

    async def get_all_events_seats(self) -> EventSeatReadShort:
        return await self.db.events_seats.get_all()

