import abc
from typing import Annotated, Literal

from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends

from db.elastic import get_elastic
from models.film import Film


class FilmStorage(abc.ABC):
    @abc.abstractmethod
    async def get_by_id(self, id: str) -> Film | None:
        raise NotImplementedError

    @abc.abstractmethod
    async def search(
        self,
        search_size: int,
        search_from: int,
        sort_key: str | None = None,
        sort_mode: Literal["asc", "desc"] | None = None,
        **kwargs,
    ) -> list[Film]:
        raise NotImplementedError


class ElasticSearchFilmStorage(FilmStorage):
    def __init__(self, elastic: Annotated[AsyncElasticsearch, Depends(get_elastic)]) -> None:
        self.elastic = elastic
        self.index = "movies"

    async def get_by_id(self, id: str):
        try:
            doc = await self.elastic.get(index=self.index, id=id)
        except NotFoundError:
            return None
        return Film(**doc["_source"])

    async def search(
        self,
        search_size: int,
        search_from: int,
        sort_key: str | None = None,
        sort_mode: Literal["asc", "desc"] | None = None,
        **kwargs,
    ):
        search_body: dict[str, int | dict] = {
            "size": search_size,
            "from": search_from,
        }

        if sort_key and sort_mode:
            search_body["sort"] = {sort_key: {"order": sort_mode, "mode": "min" if sort_mode == "asc" else "max"}}
        if kwargs.get("title"):
            search_body["query"] = {"match": {"title": kwargs["title"]}}

        if kwargs.get("genre_name"):
            search_body["query"] = {
                "bool": {
                    "filter": [
                        {"term": {"genres": kwargs["genre_name"]}},
                    ],
                },
            }

        try:
            doc = await self.elastic.search(index=self.index, body=search_body)
        except NotFoundError:
            return None

        return [Film(**hit["_source"]) for hit in doc["hits"]["hits"]]
