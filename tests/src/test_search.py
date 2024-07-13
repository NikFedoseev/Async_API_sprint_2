import pytest
from testdata import es_data_fake_10, es_data_the_star_60
from testdata.person_mocks import person_film_mock, person_mock, response_person_mock
from utils.helpers import assert_have_json

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


@pytest.mark.parametrize(
    "preload_data, query_data, expected_answer",
    [
        [
            {
                ESIndex.persons.value: [
                    person_mock(
                        {
                            "full_name": "Harrison Ford",
                        }
                    ),
                    person_mock(
                        {
                            "full_name": "Chuck Norris",
                        }
                    ),
                ],
            },
            {"name": "Harrison Ford"},
            {
                "status": 200,
                "data": [
                    response_person_mock(
                        {
                            "full_name": "Harrison Ford",
                        }
                    ),
                ],
            },
        ],
        [
            {
                ESIndex.persons.value: [
                    person_mock(
                        {
                            "full_name": "Harrison Ford",
                        }
                    ),
                    person_mock(
                        {
                            "full_name": "Chuck Norris",
                        }
                    ),
                ],
            },
            {"name": "Robert De Niro"},
            {"status": 200, "data": []},
        ],
        [
            {
                ESIndex.persons.value: [
                    person_mock({"full_name": "Harrison Ford", "films": [person_film_mock({"roles": ["actor"]})]}),
                    person_mock({"full_name": "Chuck Norris", "films": [person_film_mock({"roles": ["writer"]})]}),
                ],
            },
            {"role": "actor"},
            {
                "status": 200,
                "data": [
                    response_person_mock(
                        {"full_name": "Harrison Ford", "films": [person_film_mock({"roles": ["actor"]})]}
                    ),
                ],
            },
        ],
        [
            {
                ESIndex.persons.value: [
                    person_mock(
                        {
                            "full_name": "Harrison Ford",
                            "films": [
                                person_film_mock(
                                    {
                                        "title": "9 Muses of Star Empire",
                                    }
                                )
                            ],
                        }
                    ),
                    person_mock(
                        {
                            "full_name": "Chuck Norris",
                            "films": [
                                person_film_mock(
                                    {
                                        "title": "Other folm",
                                    }
                                )
                            ],
                        }
                    ),
                ],
            },
            {"film_title": "9 Muses of Star Empire"},
            {
                "status": 200,
                "data": [
                    response_person_mock(
                        {
                            "full_name": "Harrison Ford",
                            "films": [
                                person_film_mock(
                                    {
                                        "title": "9 Muses of Star Empire",
                                    }
                                )
                            ],
                        }
                    ),
                ],
            },
        ],
        [
            {
                ESIndex.persons.value: [
                    person_mock(
                        {
                            "full_name": "Harrison Ford",
                        }
                    ),
                    person_mock(
                        {
                            "full_name": "Chuck Norris",
                        }
                    ),
                ],
            },
            {"film_title": "Star", "page_number": -1},
            {
                "status": 422,
                "data": {
                    "detail": [
                        {
                            "type": "greater_than_equal",
                            "loc": ["query", "page_number"],
                            "msg": "Input should be greater than or equal to 1",
                            "input": "-1",
                            "ctx": {"ge": 1},
                        }
                    ]
                },
            },
        ],
        [
            {
                ESIndex.persons.value: [
                    person_mock(
                        {
                            "full_name": "Harrison Ford",
                        }
                    ),
                    person_mock(
                        {
                            "full_name": "Chuck Norris",
                        }
                    ),
                ],
            },
            {},
            {"status": 400, "data": {"detail": "query should contain at least one of filters: name, role, film_title"}},
        ],
    ],
)
@pytest.mark.asyncio()
async def test__search_persons(clear_cache, es_write_data, make_get_request, preload_data, query_data, expected_answer):
    for name, data in preload_data.items():
        data_to_load = [{"_index": name, "_id": row["id"], "_source": row} for row in data]
        await es_write_data(name, data_to_load)

    response = await make_get_request("/api/v1/persons/search", query_data)
    assert response.status_code == expected_answer["status"]
    assert_have_json(should_be=expected_answer["data"], other=response.json(), exclude_ids=True)
