import asyncio

import httpx
import pytest_asyncio
from elasticsearch import AsyncElasticsearch
from elasticsearch.helpers import async_bulk

from settings import test_settings


@pytest_asyncio.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def es_client():
    es_client = AsyncElasticsearch(hosts=test_settings.es_host, verify_certs=False)
    yield es_client
    await es_client.close()


@pytest_asyncio.fixture()
def es_write_data(es_client):
    async def inner(data: list[dict]) -> None:
        if await es_client.indices.exists(index=test_settings.es_index):
            await es_client.indices.delete(index=test_settings.es_index)
        await es_client.indices.create(index=test_settings.es_index, **test_settings.es_index_mapping)

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
        url = test_settings.service_url + method
        async_response = await async_client.get(url, params=query_data)

        return async_response

    return inner
