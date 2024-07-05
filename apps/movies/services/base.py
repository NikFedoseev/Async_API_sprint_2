import pickle
from uuid import UUID

from redis.asyncio import Redis


class BaseService:
    def __init__(self, redis: Redis) -> None:
        self.redis = redis
        self.cache_expire = 300

    @staticmethod
    def _get_complex_id_new(method: str, **kwargs) -> str:
        return method + ":" + ":".join(str(item) for item in kwargs.values() if item is not None)

    async def put_item_to_cache(self, method: str, item, **kwargs) -> None:
        await self.redis.set(self._get_complex_id_new(method=method, **kwargs), pickle.dumps(item), self.cache_expire)

    async def get_item_from_cache(self, method: str, item_id: UUID | None = None, **kwargs):
        data = await self.redis.get(self._get_complex_id_new(method=method, item_id=item_id, **kwargs))

        if not data:
            return None

        return pickle.loads(data)
