import asyncio

import httpx
import pytest_asyncio
from elasticsearch import AsyncElasticsearch
from elasticsearch.helpers import async_bulk
from redis import Redis
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
async def es_write_data(es_client):
    async def inner(index_name: ESIndex, data: list[dict]) -> None:
        if await es_client.indices.exists(index=index_name):
            await es_client.indices.delete(index=index_name)

        await es_client.indices.create(index=index_name, **get_index_config_by_name(index_name))

        _, errors = await async_bulk(client=es_client, actions=data)

        await es_client.indices.refresh(index=index_name)

        if errors:
            raise Exception("Ошибка записи данных в Elasticsearch")

    return inner


@pytest_asyncio.fixture()
async def async_client():
    async with httpx.AsyncClient() as client:
        yield client


@pytest_asyncio.fixture()
def make_get_request(async_client: httpx.AsyncClient):
    async def inner(method: str, query_data: dict | None = None) -> httpx.Response:
        url = test_settings.service.url + method
        response = await async_client.get(url, params=query_data)

        return response

    return inner


@pytest_asyncio.fixture(scope="session")
def redis_client():
    redis = Redis.from_url(test_settings.redis.url)
    yield redis
    redis.close()


@pytest_asyncio.fixture()
def clear_cache(redis_client):
    redis_client.flushdb()
    yield
