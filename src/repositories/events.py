from models.models import Event
from repositories.base import BaseRepository
from repositories.mappers.mappers import EventsDataMapper


class EventsRepository(BaseRepository):
    model = Event
    mapper = EventsDataMapper
