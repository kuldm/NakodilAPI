from models.models import Booking
from repositories.base import BaseRepository
from repositories.mappers.mappers import BookingsDataMapper


class BookingsRepository(BaseRepository):
    model = Booking
    mapper = BookingsDataMapper
