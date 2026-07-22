from infrastructure.postgres.models.models import Event
from infrastructure.postgres.repositories.base import BaseRepository
from infrastructure.postgres.repositories.mappers.mappers import EventsDataMapper


class EventsRepository(BaseRepository):
    model = Event
    mapper = EventsDataMapper
