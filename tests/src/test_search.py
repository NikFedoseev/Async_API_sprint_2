import uuid

import aiohttp
import pytest
from elasticsearch import AsyncElasticsearch
from elasticsearch.helpers import async_bulk
import time
from settings import test_settings

#  Название теста должно начинаться со слова `test_`
#  Любой тест с асинхронными вызовами нужно оборачивать декоратором `pytest.mark.asyncio`, который следит за запуском и работой цикла событий.

@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
                {'title': 'The Star'},
                {'status': 200, 'length': 50}
        ),
        (
                {'title': 'Mashed potato'},
                {'status': 200, 'length': 0}
        )
    ]
)
@pytest.mark.asyncio()
async def test_search(query_data, expected_answer):
    # 1. Генерируем данные для ES
    es_data = [
        {
            "id": str(uuid.uuid4()),
            "imdb_rating": 8.5,
            "title": "The Star",
            "description": "New World",
            "genres": ["Action", "Sci-Fi"],
            "directors_names": ["Stan"],
            "actors_names": ["Ann", "Bob"],
            "writers_names": ["Ben", "Howard"],
            "actors": [
                {"id": "ef86b8ff-3c82-4d31-ad8e-72b69f4e3f95", "name": "Ann"},
                {"id": "fb111f22-121e-44a7-b78f-b19191810fbf", "name": "Bob"},
            ],
            "writers": [
                {"id": "caf76c67-c0fe-477e-8766-3ab3ff2574b5", "name": "Ben"},
                {"id": "b45bd7bc-2e16-46d5-b125-983d356768c6", "name": "Howard"},
            ],
            "directors": [],
        }
        for _ in range(60)
    ]

    bulk_query: list[dict] = []
    for row in es_data:
        data = {"_index": "movies", "_id": row["id"]}
        data.update({"_source": row})
        bulk_query.append(data)

    # 2. Загружаем данные в ES
    es_client = AsyncElasticsearch(hosts=test_settings.es_host, verify_certs=False)
    if await es_client.indices.exists(index=test_settings.es_index):
        await es_client.indices.delete(index=test_settings.es_index)
    await es_client.indices.create(index=test_settings.es_index, **test_settings.es_index_mapping)

    updated, errors = await async_bulk(client=es_client, actions=bulk_query)

    await es_client.close()

    if errors:
        raise Exception("Ошибка записи данных в Elasticsearch")

    # 3. Запрашиваем данные из ES по API
    time.sleep(1)
    session = aiohttp.ClientSession()
    url = test_settings.service_url + "/api/v1/films/search"
    # query_data = {"title": "The Star"}
    async with session.get(url, params=query_data) as response:
        body = await response.json()
        headers = response.headers
        status = response.status
    await session.close()

    # 4. Проверяем ответ

    assert status == expected_answer.get('status')
    assert len(body) == expected_answer.get('length')
