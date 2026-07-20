from models.models import Event, Booking, Seat, EventSeat
from repositories.mappers.base import DataMapper
from schemas.events import EventRead
from schemas.bookings import CheckoutBooking, BookingAdd, BookingRead
from schemas.seats import SeatRead, EventSeatRead, EventSeatReadShort


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