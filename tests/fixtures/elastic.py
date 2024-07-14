import pytest_asyncio
from elasticsearch import AsyncElasticsearch
from elasticsearch.helpers import async_bulk
from testdata.es_mapping import get_index_config_by_name

from settings import ESIndex, test_settings


@pytest_asyncio.fixture(scope="session")
async def es_client():
    es_client = AsyncElasticsearch(hosts=test_settings.es.url, verify_certs=False)
    yield es_client
    await es_client.close()


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
async def fill_elastic_indices(es_write_data):
    async def inner(preload_data: dict[str, list[dict]]) -> None:
        for name, data in preload_data.items():
            data_to_load = [{"_index": name, "_id": row["id"], "_source": row} for row in data]
            await es_write_data(name, data_to_load)

    return inner
