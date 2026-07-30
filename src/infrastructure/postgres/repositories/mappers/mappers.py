from infrastructure.postgres.models.models import (
    Event,
    Booking,
    Seat,
    EventSeat,
    EventView,
)
from infrastructure.postgres.repositories.mappers.base import DataMapper
from schemas.bookings import BookingRead
from schemas.events import EventRead, EventViews
from schemas.seats import SeatRead, EventSeatReadShort


class EventsDataMapper(DataMapper):
    db_model = Event
    schema = EventRead


class EventViewsDataMapper(DataMapper):
    db_model = EventView
    schema = EventViews


class BookingsDataMapper(DataMapper):
    db_model = Booking
    schema = BookingRead


class SeatsDataMapper(DataMapper):
    db_model = Seat
    schema = SeatRead


class EventsSeatsMapper(DataMapper):
    db_model = EventSeat
    schema = EventSeatReadShort
