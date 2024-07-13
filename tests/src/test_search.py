import pytest
from testdata import es_data_fake_10, es_data_the_star_60

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
    await es_write_data(ESIndex.movies, bulk_query)

    response = await make_get_request("/api/v1/films/search", query_data)

    assert response.status_code == expected_answer.get("status")
    assert len(response.json()) == expected_answer.get("length")


@pytest.mark.parametrize(
    ("query_data", "expected_answer"),
    [
        (
            {"title": "The Star", "page_number": 0},
            {"status": 422, "error_message": "Input should be greater than or equal to 1"},
        ),
        (
            {"title": "The Star", "page_size": 0},
            {"status": 422, "error_message": "Input should be greater than or equal to 1"},
        ),
        (
            {"title": "The Star", "page_size": 501},
            {"status": 422, "error_message": "Input should be less than or equal to 500"},
        ),
    ],
)
@pytest.mark.asyncio()
async def test_search_incorrect_pagination(es_write_data, es_bulk_query, make_get_request, query_data, expected_answer):
    bulk_query = await es_bulk_query(index=ESIndex.movies, data=es_data_the_star_60)
    # await es_write_data(ESIndex.movies, bulk_query)
    await es_write_data(ESIndex.movies, bulk_query)

    response = await make_get_request("/api/v1/films/search", query_data)
    response_msg = response.json().get("detail")[0].get("msg")

    assert response.status_code == expected_answer.get("status")
    assert response_msg == expected_answer.get("error_message")


@pytest.mark.parametrize(
    ("query_data", "expected_answer"),
    [
        (
            {"title": "Doctor Who", "page_size": 1},
            {"status": 200, "length": 1},
        ),
        (
            {"title": "Doctor Who", "page_size": 3},
            {"status": 200, "length": 3},
        ),
        (
            {"title": "Doctor Who", "page_size": 12},
            {"status": 200, "length": 10},
        ),
    ],
)
@pytest.mark.asyncio()
async def test_search_current_page_size(es_write_data, es_bulk_query, make_get_request, query_data, expected_answer):
    bulk_query = await es_bulk_query(index=ESIndex.movies, data=es_data_fake_10 + es_data_the_star_60)
    await es_write_data(ESIndex.movies, bulk_query)

    response = await make_get_request("/api/v1/films/search", query_data)

    assert response.status_code == expected_answer.get("status")
    assert len(response.json()) == expected_answer.get("length")


@pytest.mark.skip()
@pytest.mark.asyncio()
async def test_search_with_cache(es_write_data, es_bulk_query, make_get_request, query_data, expected_answer):
    bulk_query = await es_bulk_query(index=ESIndex.movies, data=[])
    await es_write_data(ESIndex.movies, bulk_query)

    response = await make_get_request("/api/v1/films/search", query_data)

    assert response.status_code == expected_answer.get("status")
    assert len(response.json()) == expected_answer.get("length")
