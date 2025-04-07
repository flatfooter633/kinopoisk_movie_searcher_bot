import redis.asyncio as aioredis
import json
from typing import Any, Optional
from config import REDIS_HOST, REDIS_PORT, REDIS_PASSWORD

redis_url = f"redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}"

redis_client = aioredis.from_url(redis_url, encoding="utf-8", decode_responses=True)


async def get_cache(key: str) -> Optional[Any]:
    cached_result = await redis_client.get(key)
    if cached_result:
        return json.loads(cached_result)
    return None


async def set_cache(key: str, value: Any, expire: int = 604800): # время хранения - 7 дней
    await redis_client.set(key, json.dumps(value), ex=expire)
