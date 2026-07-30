from redis.asyncio import Redis

from src.config import RedisConfig


class RedisManager:
    def __init__(self, redis: Redis):
        self.client = redis

    async def close(self) -> None:
        await self.client.close()


def create_redis_manager(config: RedisConfig) -> RedisManager:
    redis = Redis.from_url(
        config.redis_url,
        decode_responses=True,
    )

    return RedisManager(redis)
