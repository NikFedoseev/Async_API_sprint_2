from functools import lru_cache
from typing import Any
from uuid import UUID

from elasticsearch import AsyncElasticsearch, NotFoundError
from redis.asyncio import Redis

from models import Genre
from services.base import BaseService
from services.deps import ElasticClient, RedisClient


class GenreService(BaseService):
    def __init__(self, elastic: AsyncElasticsearch, redis: Redis) -> None:
        super().__init__(redis)
        self.elastic = elastic

    async def get_by_id(self, genre_id: UUID) -> Genre | None:
        genre = await self.get_item_from_cache(method="genres/get_by_id", item_id=genre_id)

        if not genre:
            genre = await self._get_genre_from_elastic(genre_id)
            if not genre:
                return None
            await self.put_item_to_cache(item=genre, method="genres/get_by_id", item_id=genre_id)
        return genre

    async def get_all_genres(self) -> list[Genre]:
        query: dict[str, Any] = {"query": {"bool": {"must": []}}}
        genres = await self.get_item_from_cache(method="genres/get_all_genres")

        if not genres:
            genres = await self.elastic.search(index="genres", body=query)
            await self.put_item_to_cache(item=genres, method="genres/get_all_genres")

        return [Genre(**hit["_source"]) for hit in genres["hits"]["hits"]]

    async def _get_genre_from_elastic(self, genre_id: UUID) -> Genre | None:
        try:
            doc = await self.elastic.get(index="genres", id=str(genre_id))
        except NotFoundError:
            return None

        return Genre(**doc["_source"])


@lru_cache(maxsize=1)
def get_genre_service(elastic: ElasticClient, redis: RedisClient) -> GenreService:
    return GenreService(elastic, redis)
