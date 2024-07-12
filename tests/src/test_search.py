import time

import pytest
from testdata import es_data_the_star_60

from settings import ESIndex


@pytest.mark.parametrize(
    ("query_data", "expected_answer"),
    [
        ({"title": "The Star"}, {"status": 200, "length": 50}),
        ({"title": "Mashed potato"}, {"status": 200, "length": 0}),
    ],
)
@pytest.mark.asyncio()
async def test_search(es_write_data, es_bulk_query, make_get_request, query_data, expected_answer):
    bulk_query = await es_bulk_query(index=ESIndex.movies, data=es_data_the_star_60)
    await es_write_data(bulk_query)

    time.sleep(1)  # сам по себе тест моргающий, надо бы какой нибудь tenacity, но пока так
    response = await make_get_request("/api/v1/films/search", query_data)

    assert response.status_code == expected_answer.get("status")
    assert len(response.json()) == expected_answer.get("length")
