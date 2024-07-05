from functools import lru_cache
from uuid import UUID

from elasticsearch import AsyncElasticsearch, NotFoundError
from models import Film
from models.genre import Genre
from redis.asyncio import Redis
from services.base import BaseService
from services.deps import ElasticClient, RedisClient


class FilmService(BaseService):
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        super().__init__(redis)
        self.elastic = elastic

    async def get_by_id(self, film_id: UUID) -> Film | None:
        film = await self.get_item_from_cache(method="films/get_by_id", item_id=film_id)

        if not film:
            film = await self._get_film_from_elastic(film_id)
            if not film:
                return None

            await self.put_item_to_cache(item=film, method="films/get_by_id", item_id=film_id)

        return film

    async def get_all(
        self,
        sort: str | None,
        genre: str | None,
        page_size: int,
        page_number: int,
    ) -> list[Film] | None:
        sort_field = self._make_sort_field(sort)
        query = await self._make_genre_query(genre)

        films = await self.get_item_from_cache(
            method="films/get_all", sort=sort, genre=genre, page_size=page_size, page_number=page_number
        )

        if not films:
            films = await self._get_films_from_elastic(
                search_size=page_size, search_from=(page_number - 1) * page_size, sort=sort_field, query=query
            )
            await self.put_item_to_cache(
                item=films, method="films/get_all", sort=sort, genre=genre, page_size=page_size, page_number=page_number
            )

        return films

    async def search(
        self,
        title: str,
        page_size: int,
        page_number: int,
    ) -> list[Film] | None:
        films = await self.get_item_from_cache(
            method="films/search", title=title, page_size=page_size, page_number=page_number
        )

        if not films:
            films = await self._get_films_from_elastic(
                search_size=page_size,
                search_from=(page_number - 1) * page_size,
                query={"match": {"title": title}},
            )
            await self.put_item_to_cache(
                item=films, method="films/search", title=title, page_size=page_size, page_number=page_number
            )

        return films

    def _make_sort_field(self, sort: str | None):
        if not sort:
            return None

        sort_order = sort[0:1]

        if sort_order.startswith("-"):
            sort_key = sort[1:]
            order = "asc"
            mode = "min"
        else:
            sort_key = sort
            order = "desc"
            mode = "max"

        return {sort_key: {"order": order, "mode": mode}}

    async def _make_genre_query(self, genre: str | None):
        if not genre:
            return None

        try:
            doc = await self.elastic.get(index="genres", id=genre)
        except NotFoundError:
            return None

        genre_name = Genre(**doc["_source"]).name

        return {
            "bool": {
                "filter": [
                    {"term": {"genres": genre_name}},
                ],
            },
        }

    async def _get_film_from_elastic(self, film_id: UUID) -> Film | None:
        try:
            doc = await self.elastic.get(index="movies", id=str(film_id))
        except NotFoundError:
            return None
        return Film(**doc["_source"])

    async def _get_films_from_elastic(
        self, search_size: int, search_from: int, sort: dict | None = None, query: dict | None = None
    ) -> list[Film] | None:
        search_body: dict[str, int | dict] = {
            "size": search_size,
            "from": search_from,
        }

        if sort:
            search_body["sort"] = sort
        if query:
            search_body["query"] = query

        try:
            doc = await self.elastic.search(index="movies", body=search_body)
        except NotFoundError:
            return None

        return [Film(**hit["_source"]) for hit in doc["hits"]["hits"]]


@lru_cache(maxsize=1)
def get_film_service(redis: RedisClient, elastic: ElasticClient) -> FilmService:
    return FilmService(redis, elastic)
