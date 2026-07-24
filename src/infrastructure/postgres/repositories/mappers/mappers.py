from infrastructure.postgres.models.models import Event, Booking, Seat, EventSeat
from infrastructure.postgres.repositories.mappers.base import DataMapper
from schemas.bookings import BookingRead
from schemas.events import EventRead
from schemas.seats import SeatRead, EventSeatReadShort


class EventsDataMapper(DataMapper):
    db_model = Event
    schema = EventRead


class BookingsDataMapper(DataMapper):
    db_model = Booking
    schema = BookingRead


class SeatsDataMapper(DataMapper):
    db_model = Seat
    schema = SeatRead


class EventsSeatsMapper(DataMapper):
    db_model = EventSeat
    schema = EventSeatReadShort
