import abc
import pickle
from collections.abc import Callable
from typing import Annotated, Any

import orjson
from fastapi import Depends
from redis.asyncio import Redis

from db.redis import get_redis


class Cache(abc.ABC):
    @abc.abstractmethod
    async def get(self, key: str) -> Any:
        raise NotImplementedError

    @abc.abstractmethod
    async def set(self, key: str, value: Any, expire: int):
        raise NotImplementedError


class RedisCache(Cache):
    def __init__(self, redis: Annotated[Redis, Depends(get_redis)]) -> None:
        self.redis = redis

    async def get(self, key: str):
        if value := await self.redis.get(key):
            return pickle.loads(value)
        return None

    async def set(self, key: str, value: Any, expire: int):
        await self.redis.set(key, pickle.dumps(value), expire)


def cached_method(cache: Callable[[Any], Cache], expire: int):
    def decorator(func: Callable):
        def get_cache_key(*args, **kwargs):
            cache_key = func.__name__
            if args:
                cache_key += orjson.dumps(args).decode()
            if kwargs:
                cache_key += orjson.dumps(kwargs).decode()

            return cache_key

        async def wrapper(self, *args, **kwargs):
            c = cache(self)
            cache_key = get_cache_key(*args, **kwargs)
            if cached_value := await c.get(cache_key):
                return cached_value

            res = await func(self, *args, **kwargs)

            await c.set(cache_key, res, expire)
            return res

        return wrapper

    return decorator
