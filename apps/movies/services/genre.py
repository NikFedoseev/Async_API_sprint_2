from functools import lru_cache
from uuid import UUID

from cache import Cache, cached_method
from storages.genre import GenreStorage

from models import Genre
from services.deps import ElasticSearchGenreStorage, RedisCache


class GenreService:
    def __init__(self, cache: Cache, storage: GenreStorage) -> None:
        self.cache = cache
        self.storage = storage

    @cached_method(lambda self: self.cache, expire=300)
    async def get_by_id(self, genre_id: UUID) -> Genre | None:
        return await self.storage.get_by_id(id=str(genre_id))

    @cached_method(lambda self: self.cache, expire=300)
    async def get_all_genres(self) -> list[Genre]:
        return await self.storage.get_all()


@lru_cache(maxsize=1)
def get_genre_service(cache: RedisCache, storage: ElasticSearchGenreStorage) -> GenreService:
    return GenreService(cache, storage)
