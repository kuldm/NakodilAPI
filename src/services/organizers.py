import asyncio

from exceptions import (
    EventDoesNotBelongToOrganizerException,
    EventNotFoundException,
)
from models.models import Event, SeatStatus, Booking, BookingStatus
from schemas.events import EventRead, EventCreate, EventAdd
from schemas.schemas import EventDashboard, OccupancyDashboard, SalesDashboard
from services.base import BaseService


class OrganizersService(BaseService):
    async def get_organizer_events(self, organizer_id: int) -> list[EventRead]:
        return await self.db.events.get_filtered(Event.organizer_id == organizer_id)

    async def create_organizer_event(
        self, organizer_id: int, payload: EventCreate
    ) -> None:
        event = await self.db.events.add(
            EventAdd(**payload.model_dump(), organizer_id=organizer_id)
        )
        await self.db.commit()
        return event

    async def get_event_dashboard(
        self, event_id: int, organizer_id: int
    ) -> EventDashboard:
        event = await self.db.events.get_one_or_none(id=event_id)
        if event is None:
            raise EventNotFoundException
        if event.organizer_id == organizer_id:
            async with asyncio.TaskGroup() as tg:
                occupancy_task = tg.create_task(self._calculate_occupancy(event_id))
                sales_task = tg.create_task(self._calculate_sales(event_id))

            occupancy: OccupancyDashboard = occupancy_task.result()
            sales: SalesDashboard = sales_task.result()

            sales.sold_tickets = occupancy.sold

            dashboard = EventDashboard(
                event_title=event.title,
                starts_at=event.starts_at,
                sales=sales,
                occupancy=occupancy,
            )
            return dashboard

        else:
            raise EventDoesNotBelongToOrganizerException

    async def _calculate_occupancy(self, event_id: int) -> OccupancyDashboard:
        async with self.db.transaction() as db:
            event_seats = await db.events_seats.get_event_seats_by_event_id(event_id)

            if not event_seats:
                return OccupancyDashboard(total=0, available=0, reserved=0, sold=0, occupancy_percent=0.0)

        total = len(event_seats)
        available = sum(
            1 for seat in event_seats if seat.status == SeatStatus.available
        )
        reserved = sum(1 for seat in event_seats if seat.status == SeatStatus.reserved)
        sold = sum(1 for seat in event_seats if seat.status == SeatStatus.sold)
        occupancy_percent = ((sold + reserved) / total) * 100 if total else 0

        occupancy = OccupancyDashboard(
            total=total,
            available=available,
            reserved=reserved,
            sold=sold,
            occupancy_percent=occupancy_percent,
        )
        return occupancy

    async def _calculate_sales(self, event_id: int) -> SalesDashboard:
        async with self.db.transaction() as db:
            bookings = await db.bookings.get_filtered(Booking.event_id == event_id)

            if not bookings:
                return SalesDashboard(paid_orders=0, sold_tickets=0, revenue=0, average_order=0)

        paid_orders = sum(
            1 for booking in bookings if booking.status == BookingStatus.paid
        )
        revenue = sum(booking.amount for booking in bookings)
        average_order = revenue // len(bookings) if bookings else 0

        sales = SalesDashboard(
            paid_orders=paid_orders,
            sold_tickets=0,
            revenue=revenue,
            average_order=average_order,
        )
        return sales
