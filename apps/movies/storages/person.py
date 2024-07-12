import abc
from typing import Annotated, Any

from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends

from db.elastic import get_elastic
from models.person import Person


class PersonStorage(abc.ABC):
    @abc.abstractmethod
    async def get_by_id(self, id: str) -> Person | None:
        raise NotImplementedError

    @abc.abstractmethod
    async def search(
        self,
        search_size: int,
        search_from: int,
        name: str | None = None,
        role: str | None = None,
        film_title: str | None = None,
    ) -> list[Person]:
        raise NotImplementedError


class ElasticPersonFilmStorage(PersonStorage):
    def __init__(self, elastic: Annotated[AsyncElasticsearch, Depends(get_elastic)]) -> None:
        self.elastic = elastic
        self.index = "persons"

    async def get_by_id(self, id: str):
        try:
            doc = await self.elastic.get(index=self.index, id=id)
        except NotFoundError:
            return None
        return Person(**doc["_source"])

    async def search(
        self,
        search_size: int,
        search_from: int,
        name: str | None = None,
        role: str | None = None,
        film_title: str | None = None,
    ):
        query: dict[str, Any] = {"bool": {"must": []}}
        search_body: dict[str, int | dict] = {
            "size": search_size,
            "from": search_from,
        }

        if name:
            query["bool"]["must"].append({"match": {"full_name": name}})
        if role:
            query["bool"]["must"].append({"nested": {"path": "films", "query": {"match": {"films.roles": role}}}})
        if film_title:
            query["bool"]["must"].append({"nested": {"path": "films", "query": {"match": {"films.title": film_title}}}})

        search_body["query"] = query

        try:
            doc = await self.elastic.search(index=self.index, body=search_body)
        except NotFoundError:
            return None

        return [Person(**hit["_source"]) for hit in doc["hits"]["hits"]]
