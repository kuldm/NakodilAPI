from models.models import Booking
from repositories.base import BaseRepository
from repositories.mappers.mappers import BookingsDataMapper
from repositories.seats import SeatsRepository
from schemas.bookings import BookingCreate, CheckoutBooking


class BookingsRepository(BaseRepository):
    model = Booking
    mapper = BookingsDataMapper

    async def reserved_booking(
        self, user_id: int, event_id, payload: BookingCreate
    ) -> CheckoutBooking:
        """Добавляет бронирование мест для пользователя."""
        seats = await SeatsRepository().get_all()

