import uuid

import pytest


@pytest.mark.parametrize(
    ("query_data", "expected_answer"),
    [
        ({"title": "The Star"}, {"status": 200, "length": 50}),
        ({"title": "Mashed potato"}, {"status": 200, "length": 0}),
    ],
)
@pytest.mark.asyncio()
async def test_search(es_write_data, make_get_request, query_data, expected_answer):
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
    await es_write_data(bulk_query)

    # 3. Запрашиваем данные из ES по API
    response = await make_get_request("/api/v1/films/search", query_data)

    # 4. Проверяем ответ
    assert response.status_code == expected_answer.get("status")
    assert len(response.json()) == expected_answer.get("length")
