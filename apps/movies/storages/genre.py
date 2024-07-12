import abc
from typing import Annotated

from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends

from db.elastic import get_elastic
from models.genre import Genre


class GenreStorage(abc.ABC):
    @abc.abstractmethod
    async def get_by_id(self, id: str) -> Genre | None:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_all(self) -> list[Genre]:
        raise NotImplementedError


class ElasticSearchGenreStorage(GenreStorage):
    def __init__(self, elastic: Annotated[AsyncElasticsearch, Depends(get_elastic)]) -> None:
        self.elastic = elastic
        self.index = "genres"

    async def get_by_id(self, id: str):
        try:
            doc = await self.elastic.get(index=self.index, id=id)
        except NotFoundError:
            return None
        return Genre(**doc["_source"])

    async def get_all(self):
        doc = await self.elastic.search(index=self.index, body={"query": {"bool": {"must": []}}})
        return [Genre(**hit["_source"]) for hit in doc["hits"]["hits"]]
