from typing import AsyncGenerator

import redis.asyncio as redis

from app.settings import Settings


async def get_redis_connection() -> redis.Redis:
    settings = Settings()
    return redis.Redis(
        host=settings.CACHE_HOST,
        port=settings.CACHE_PORT,
        db=settings.CACHE_DB,
        password=None,
        decode_responses=True,
    )


async def get_cache_session() -> AsyncGenerator[redis.Redis, None]:
    cache_session = await get_redis_connection()
    try:
        yield cache_session
    finally:
        await cache_session.close()
