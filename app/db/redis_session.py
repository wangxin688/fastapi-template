from datetime import datetime
from typing import Any

import orjson
import redis.asyncio as redis

from app.core.config import settings


def default(obj):
    if isinstance(obj, datetime):
        return int(obj.timestamp())


async def init_redis_pool(db: int) -> redis.Redis:
    redis_c = await redis.from_url(
        settings.REDIS_DSN, encoding="utf-8", db=db, decode_responses=True
    )
    return redis_c


class RedisClient:
    def __init__(self, redis: redis.Redis) -> None:
        self._redis = redis

    async def set(self, key: str, data: Any, expire: int = 1800):
        return self._redis.set(key, orjson.dumps(data, default=default), ex=expire)

    async def get(self, key: str):
        result = await self._redis.get(key)
        if result:
            return orjson.loads(result)
        return result

    async def delete(self, key: str):
        return await self._redis.delete(key)

    async def ttl(self, key):
        return self.r.ttl(key)
