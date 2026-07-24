from datetime import datetime
from typing import List

from sqlalchemy import update, select

from infrastructure.postgres.models.models import Seat, EventSeat, SeatStatus
from infrastructure.postgres.repositories.base import BaseRepository
from infrastructure.postgres.repositories.mappers.mappers import (
    SeatsDataMapper,
    EventsSeatsMapper,
)
from schemas.seats import EventSeatRead, EventSeatReadShort


class SeatsRepository(BaseRepository):
    model = Seat
    mapper = SeatsDataMapper

    async def get_filtered_by_id(self, ids: List[int]):
        return await self.get_filtered(self.model.id.in_(ids))


class EventsSeatsRepository(BaseRepository):
    model = EventSeat
    mapper = EventsSeatsMapper

    async def get_event_seats_by_event_id(
        self, event_id: int
    ) -> List[EventSeatReadShort]:
        return await self.get_filtered(self.model.event_id == event_id)

    async def lock_for_reserve(self, event_id: int, seat_ids: List[int]):
        query = (
            select(EventSeat)
            .where(EventSeat.event_id == event_id, EventSeat.id.in_(seat_ids))
            .with_for_update()
        )
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def mark_reserved(
        self, seat_ids: List[int], booking_id: int, reserved_until: datetime
    ):
        query = (
            update(EventSeat)
            .where(EventSeat.id.in_(seat_ids))
            .values(
                status=SeatStatus.reserved,
                booking_id=booking_id,
                reserved_until=reserved_until,
            )
        )
        await self.session.execute(query)

    async def get_relation_seat_and_event_seats_by_event_id(
        self, event_id: int
    ) -> List[EventSeatRead]:
        query = (
            select(
                EventSeat.id,
                EventSeat.event_id,
                EventSeat.seat_id,
                Seat.sector,
                Seat.row,
                Seat.number,
                Seat.x,
                Seat.y,
                EventSeat.price,
                EventSeat.status,
                EventSeat.reserved_until,
                EventSeat.booking_id,
            )
            .join(Seat, Seat.id == EventSeat.seat_id)
            .where(EventSeat.event_id == event_id)
        )
        result = await self.session.execute(query)
        return [
            EventSeatRead(
                id=row.id,
                event_id=row.event_id,
                seat_id=row.seat_id,
                sector=row.sector,
                row=row.row,
                number=row.number,
                x=row.x,
                y=row.y,
                price=row.price,
                status=row.status,
                reserved_until=row.reserved_until,
                booking_id=row.booking_id,
            )
            for row in result.all()
        ]
