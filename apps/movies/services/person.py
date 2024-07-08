from functools import lru_cache
from uuid import UUID

from cache import Cache, cached_method
from models import Person, PersonFilm
from services.deps import ElasticPersonFilmStorage, ElasticSearchFilmStorage, RedisCache
from storages.film import FilmStorage
from storages.person import PersonStorage


class PersonService:
    def __init__(self, cache: Cache, storage: PersonStorage, film_storage: FilmStorage) -> None:
        self.cache = cache
        self.storage = storage
        self.film_storage = film_storage

    @cached_method(lambda self: self.cache, expire=300)
    async def search(
        self,
        page_size: int,
        page_number: int,
        name: str | None = None,
        role: str | None = None,
        film_title: str | None = None,
    ) -> list[Person]:
        return await self.storage.search(
            search_size=page_size,
            search_from=(page_number - 1) * page_size,
            name=name,
            role=role,
            film_title=film_title,
        )

    @cached_method(lambda self: self.cache, expire=300)
    async def get_by_id(self, person_id: UUID) -> Person | None:
        return await self.storage.get_by_id(id=str(person_id))

    @cached_method(lambda self: self.cache, expire=300)
    async def get_films(self, person_id: UUID, page_size: int, page_number: int) -> list[PersonFilm]:
        person = await self.storage.get_by_id(id=str(person_id))
        if not person:
            return []

        return person.films[(page_number - 1) * page_size : page_number * page_size]


@lru_cache(maxsize=1)
def get_person_service(
    cache: RedisCache, storage: ElasticPersonFilmStorage, film_storage: ElasticSearchFilmStorage
) -> PersonService:
    return PersonService(cache, storage, film_storage)
