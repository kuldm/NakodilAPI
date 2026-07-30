from sqlalchemy.dialects.postgresql import insert

from infrastructure.postgres.models.models import Event, EventView
from infrastructure.postgres.repositories.base import BaseRepository
from infrastructure.postgres.repositories.mappers.mappers import (
    EventsDataMapper,
    EventViewsDataMapper,
)
from schemas.events import EventViews


class EventsRepository(BaseRepository):
    model = Event
    mapper = EventsDataMapper


class EventViewsRepository(BaseRepository):
    model = EventView
    mapper = EventViewsDataMapper

    async def update_event_views_bulk(self, event_views: list[EventViews]):
        if not event_views:
            return

        stmt = insert(self.model).values([item.model_dump() for item in event_views])

        stmt = stmt.on_conflict_do_update(
            index_elements=[self.model.event_id],
            set_={
                "views_count": self.model.views_count + stmt.excluded.views_count,
            },
        )
        await self.session.execute(stmt)
