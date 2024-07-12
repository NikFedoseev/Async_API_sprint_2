from functools import lru_cache
from typing import Literal
from uuid import UUID

from cache import Cache, cached_method
from storages.film import FilmStorage
from storages.genre import GenreStorage

from models import Film
from services.deps import ElasticSearchFilmStorage, ElasticSearchGenreStorage, RedisCache


class FilmService:
    def __init__(self, cache: Cache, storage: FilmStorage, genre_storage: GenreStorage):
        self.storage = storage
        self.genre_storage = genre_storage
        self.cache = cache

    @cached_method(lambda self: self.cache, expire=300)
    async def get_by_id(self, film_id: UUID) -> Film | None:
        return await self.storage.get_by_id(id=str(film_id))

    @cached_method(lambda self: self.cache, expire=300)
    async def get_all(
        self,
        sort: str | None,
        genre_id: str | None,
        page_size: int,
        page_number: int,
    ) -> list[Film] | None:
        sort_key, sort_mode = self._get_sort_params(sort)
        genre_name = await self._get_genre_name(genre_id)

        return await self.storage.search(
            search_size=page_size,
            search_from=(page_number - 1) * page_size,
            sort_key=sort_key,
            sort_mode=sort_mode,
            genre_name=genre_name,
        )

    @cached_method(lambda self: self.cache, expire=300)
    async def search(
        self,
        title: str,
        page_size: int,
        page_number: int,
    ) -> list[Film] | None:
        return await self.storage.search(search_size=page_size, search_from=(page_number - 1) * page_size, title=title)

    def _get_sort_params(self, sort: str | None) -> tuple[str | None, Literal["asc", "desc"] | None]:
        if not sort:
            return None, None

        if sort[0:1].startswith("-"):
            return sort[1:], "asc"

        return sort, "desc"

    async def _get_genre_name(self, genre_id: str | None):
        if not genre_id:
            return None

        if genre := await self.genre_storage.get_by_id(id=genre_id):
            return genre.name


@lru_cache(maxsize=1)
def get_film_service(
    cache: RedisCache, storage: ElasticSearchFilmStorage, genre_storage: ElasticSearchGenreStorage
) -> FilmService:
    return FilmService(cache=cache, storage=storage, genre_storage=genre_storage)
