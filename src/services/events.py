from schemas.schemas import EventRead
from services.base import BaseService


class EventsService(BaseService):
    async def get_all_events(self) -> list[EventRead]:
        return await self.db.events.get_all()