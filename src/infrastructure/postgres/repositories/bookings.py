from infrastructure.postgres.models.models import Booking
from infrastructure.postgres.repositories.base import BaseRepository
from infrastructure.postgres.repositories.mappers.mappers import BookingsDataMapper


class BookingsRepository(BaseRepository):
    model = Booking
    mapper = BookingsDataMapper
