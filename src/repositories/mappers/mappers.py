from models.models import Event
from repositories.mappers.base import DataMapper
from schemas.schemas import EventRead


class EventsDataMapper(DataMapper):
    db_model = Event
    schema = EventRead