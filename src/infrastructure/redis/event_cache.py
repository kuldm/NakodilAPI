import random

from infrastructure.redis.manager import RedisManager
from schemas.events import EventRead


class EventCache:
    def __init__(self, redis: RedisManager) -> None:
        self._client = redis.client

    def _get_event_key(self, event_id: int) -> str:
        return f"event:{event_id}"

    async def get_event(self, event_id: int) -> EventRead | None:
        value = await self._client.get(self._get_event_key(event_id))

        if value is None:
            return None

        return EventRead.model_validate_json(value)

    async def set_event(
        self, event: EventRead, ttl: int | None = None
    ) -> None:
        if ttl is None:
            ttl = random.randint(300, 360)

        await self._client.set(
            self._get_event_key(event.id),
            event.model_dump_json(),
            ex=ttl
        )
