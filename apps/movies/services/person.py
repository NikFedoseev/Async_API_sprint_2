from functools import lru_cache
from typing import Any
from uuid import UUID

from elasticsearch import AsyncElasticsearch, NotFoundError
from redis.asyncio import Redis

from models import Person, PersonFilm
from services.base import BaseService
from services.deps import ElasticClient, RedisClient


class PersonService(BaseService):
    def __init__(self, elastic: AsyncElasticsearch, redis: Redis) -> None:
        super().__init__(redis)
        self.elastic = elastic

    async def search(
        self,
        page_size: int,
        page_number: int,
        name: str | None = None,
        role: str | None = None,
        film_title: str | None = None,
    ) -> list[Person]:
        query: dict[str, Any] = {"query": {"bool": {"must": []}}}

        query["from"] = (page_number - 1) * page_size
        query["size"] = page_size

        if name:
            query["query"]["bool"]["must"].append({"match": {"full_name": name}})
        if role:
            query["query"]["bool"]["must"].append(
                {"nested": {"path": "films", "query": {"match": {"films.roles": role}}}}
            )
        if film_title:
            query["query"]["bool"]["must"].append(
                {"nested": {"path": "films", "query": {"match": {"films.title": film_title}}}}
            )

        data = await self.get_item_from_cache(
            method="persons/search",
            page_size=page_size,
            page_number=page_number,
            name=name,
            role=role,
            film_title=film_title,
        )
        if not data:
            data = await self.elastic.search(index="persons", body=query)
            await self.put_item_to_cache(
                item=data,
                method="persons/search",
                page_size=page_size,
                page_number=page_number,
                name=name,
                role=role,
                film_title=film_title,
            )

        return [Person(**hit["_source"]) for hit in data["hits"]["hits"]]

    async def get_by_id(self, person_id: UUID) -> Person | None:
        person = await self.get_item_from_cache(method="persons/get_by_id", item_id=person_id)

        if not person:
            person = await self._get_person_from_elastic(person_id)
            if not person:
                return None

            await self.put_item_to_cache(method="persons/get_by_id", item=person, item_id=person_id)

        return person

    async def get_films(self, person_id: UUID, page_size: int, page_number: int) -> list[PersonFilm]:
        person = await self.get_item_from_cache(
            method="persons/get_films", item_id=person_id, page_size=page_size, page_number=page_number
        )

        if not person:
            person = await self.get_by_id(person_id)

            if not person:
                return []
            await self.put_item_to_cache(
                method="persons/get_films", item=person, item_id=person_id, page_size=page_size, page_number=page_number
            )

        return person.films[(page_number - 1) * page_size : page_number * page_size]

    async def _get_person_from_elastic(self, person_id: UUID) -> Person | None:
        try:
            doc = await self.elastic.get(index="persons", id=str(person_id))
        except NotFoundError:
            return None

        return Person(**doc["_source"])


@lru_cache(maxsize=1)
def get_person_service(elastic: ElasticClient, redis: RedisClient) -> PersonService:
    return PersonService(elastic, redis)
