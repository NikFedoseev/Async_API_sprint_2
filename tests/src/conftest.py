import pytest_asyncio
from elasticsearch import AsyncElasticsearch
from elasticsearch.helpers import async_bulk
from settings import test_settings


@pytest_asyncio.fixture(name='es_write_data')
def es_write_data():
    async def inner(data: list[dict]):
        es_client = AsyncElasticsearch(hosts=test_settings.es_host, verify_certs=False)
        if await es_client.indices.exists(index=test_settings.es_index):
            await es_client.indices.delete(index=test_settings.es_index)
        await es_client.indices.create(index=test_settings.es_index, **test_settings.es_index_mapping)

        updated, errors = await async_bulk(client=es_client, actions=data)

        await es_client.close()

        if errors:
            raise Exception('Ошибка записи данных в Elasticsearch')
    return inner