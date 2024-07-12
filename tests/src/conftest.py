import asyncio

import httpx
import pytest_asyncio
from elasticsearch import AsyncElasticsearch
from elasticsearch.helpers import async_bulk
from testdata import get_index_config_by_name

from settings import ESIndex, test_settings


@pytest_asyncio.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def es_client():
    es_client = AsyncElasticsearch(hosts=test_settings.es.url, verify_certs=False)
    yield es_client
    await es_client.close()


@pytest_asyncio.fixture()
def es_bulk_query():
    async def inner(index: ESIndex, data: list[dict]) -> list[dict]:
        bulk_query: list[dict] = []
        for row in data:
            data = {"_index": index, "_id": row["id"]}
            data.update({"_source": row})
            bulk_query.append(data)

        return bulk_query

    return inner


@pytest_asyncio.fixture()
def es_write_data(es_client):
    async def inner(data: list[dict]) -> None:
        if await es_client.indices.exists(index=ESIndex.movies):
            await es_client.indices.delete(index=ESIndex.movies)
        await es_client.indices.create(index=ESIndex.movies, **get_index_config_by_name(ESIndex.movies))

        updated, errors = await async_bulk(client=es_client, actions=data)

        if errors:
            raise Exception("Ошибка записи данных в Elasticsearch")

    return inner


@pytest_asyncio.fixture()
async def async_client():
    async with httpx.AsyncClient() as client:
        yield client


@pytest_asyncio.fixture()
def make_get_request(async_client: httpx.AsyncClient):
    async def inner(method: str, query_data: dict) -> httpx.Response:
        url = test_settings.service.url + method
        response = await async_client.get(url, params=query_data)

        return response

    return inner
