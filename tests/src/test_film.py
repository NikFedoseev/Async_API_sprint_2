import pytest
from http import HTTPStatus
from settings import ESIndex
from testdata.film_mocks import film_mock, response_film_mock, response_detailed_film_mock
from testdata.genre_mocks import genre_mock
from utils.helpers import assert_have_json


@pytest.mark.parametrize('preload_data, film_id, expected_answer', [
    [
        {
            ESIndex.movies.value: [
                film_mock({
                    'id': '3d8d9bf5-0d90-4353-88ba-4ccc5d2c07ff',
                    'title': 'Matrix',
                }),
                film_mock({
                    'id': '120a21cf-9097-479e-904a-13dd7198c1dd',
                    'title': 'Fight Club',
                }),
            ],
        },
        '3d8d9bf5-0d90-4353-88ba-4ccc5d2c07ff',
        {
            'status': HTTPStatus.OK,
            'data': response_detailed_film_mock({
                'id': '3d8d9bf5-0d90-4353-88ba-4ccc5d2c07ff',
                'title': 'Matrix',
            })
        }
    ],
    [
        {
            ESIndex.movies.value: [
                film_mock({
                    'id': '3d8d9bf5-0d90-4353-88ba-4ccc5d2c07ff',
                    'title': 'Matrix',
                }),
                film_mock({
                    'id': '120a21cf-9097-479e-904a-13dd7198c1dd',
                    'title': 'Fight Club',
                }),
            ],
        },
        '123',
        {
            'status': HTTPStatus.UNPROCESSABLE_ENTITY,
            'data': {
                'detail': [
                    {
                        'type': 'uuid_parsing',
                        'loc': ['path', 'film_id'],
                        'msg': 'Input should be a valid UUID, invalid length: expected length 32 for simple format, found 3',
                        'input': '123',
                        'ctx': {'error': 'invalid length: expected length 32 for simple format, found 3'}
                    }
                ]
            }
        }
    ],
    [
        {
            ESIndex.movies.value: [
                film_mock({
                    'id': '3d8d9bf5-0d90-4353-88ba-4ccc5d2c07ff',
                    'title': 'Matrix',
                }),
                film_mock({
                    'id': '120a21cf-9097-479e-904a-13dd7198c1dd',
                    'title': 'Fight Club',
                }),
            ],
        },
        '8c0d6810-d1fd-40bd-b221-3006e6f21da5',
        {
            'status': HTTPStatus.NOT_FOUND,
            'data': {
                'detail': 'Film not found'
            }
        }
    ],
])
@pytest.mark.asyncio()
async def test__film_details(
    clear_cache,
    fill_elastic_indices,
    make_get_request,
    preload_data,
    film_id,
    expected_answer
):
    await fill_elastic_indices(preload_data)
    
    response = await make_get_request(f"/api/v1/films/{film_id}")
    assert response.status_code == expected_answer["status"]
    assert_have_json(
        should_be=expected_answer['data'],
        other=response.json(),
        exclude_ids=True
    )


@pytest.mark.parametrize('preload_data, film_id, expected_answer', [
    [
        {
            ESIndex.movies.value: [
                film_mock({
                    'id': '3d8d9bf5-0d90-4353-88ba-4ccc5d2c07ff',
                    'title': 'Matrix',
                }),
                film_mock({
                    'id': '120a21cf-9097-479e-904a-13dd7198c1dd',
                    'title': 'Fight Club',
                }),
            ],
        },
        '3d8d9bf5-0d90-4353-88ba-4ccc5d2c07ff',
        {
            'status': HTTPStatus.OK,
            'data': response_detailed_film_mock({
                'id': '3d8d9bf5-0d90-4353-88ba-4ccc5d2c07ff',
                'title': 'Matrix',
            })
        }
    ],
    [
        {
            ESIndex.movies.value: [],
        },
        '3d8d9bf5-0d90-4353-88ba-4ccc5d2c07ff',
        {
            'status': HTTPStatus.OK,
            'data': response_detailed_film_mock({
                'id': '3d8d9bf5-0d90-4353-88ba-4ccc5d2c07ff',
                'title': 'Matrix',
            })
        }
    ],
])
@pytest.mark.asyncio()
async def test__film_details_cache(
    fill_elastic_indices,
    make_get_request,
    preload_data,
    film_id,
    expected_answer
):
    await fill_elastic_indices(preload_data)
    
    response = await make_get_request(f"/api/v1/films/{film_id}")
    assert response.status_code == expected_answer["status"]
    assert_have_json(
        should_be=expected_answer['data'],
        other=response.json(),
        exclude_ids=True
    )


@pytest.mark.parametrize('preload_data, query_data, expected_answer',[
    [
        {
            ESIndex.movies.value: [
                film_mock({
                    'title': 'Matrix',
                }),
                film_mock({
                    'title': 'Fight Club',
                }),
            ],
        },
        {},
        {
            'status': HTTPStatus.OK,
            'data': [
                response_film_mock({
                    'title': 'Matrix',
                }),
                response_film_mock({
                    'title': 'Fight Club',
                }),
            ]
        }
    ],
    [
        {
            ESIndex.movies.value: [
                film_mock({
                    'title': 'Matrix',
                    'genres': ['Action'],
                }),
                film_mock({
                    'title': 'Fight Club',
                    'genres': ['Action'],
                }),
                film_mock({
                    'title': 'Other film',
                    'genres': ['Fantasy'],
                }),
            ],
            ESIndex.genres.value: [
                genre_mock({
                    'id': '2f89e116-4827-4ff4-853c-b6e058f71e31',
                    'name': 'Action',
                }),
                
            ],
        },
        {
            'genre': '2f89e116-4827-4ff4-853c-b6e058f71e31'
        },
        {
            'status': HTTPStatus.OK,
            'data': [
                response_film_mock({
                    'title': 'Matrix',
                }),
                response_film_mock({
                    'title': 'Fight Club',
                }),
            ]
        }
    ],
    [
        {
            ESIndex.movies.value: [
                film_mock({
                    'title': 'Matrix',
                    'genres': ['Action'],
                }),
                film_mock({
                    'title': 'Fight Club',
                    'genres': ['Action'],
                }),
                film_mock({
                    'title': 'Other film',
                    'genres': ['Fantasy'],
                }),
            ],
            ESIndex.genres.value: [
                genre_mock({
                    'id': '2f89e116-4827-4ff4-853c-b6e058f71e31',
                    'name': 'Action',
                }),
                
            ],
        },
        {
            'genre': '2f89e116-4827-4ff4-853c-b6e058f71e31',
            'page_size': 1,
            'page_number': 1,
        },
        {
            'status': HTTPStatus.OK,
            'data': [
                response_film_mock({
                    'title': 'Matrix',
                }),
            ]
        }
    ],
    [
        {
            ESIndex.movies.value: [
                film_mock({
                    'title': 'Matrix',
                    'genres': ['Action'],
                }),
                film_mock({
                    'title': 'Fight Club',
                    'genres': ['Action'],
                }),
                film_mock({
                    'title': 'Other film',
                    'genres': ['Fantasy'],
                }),
            ],
            ESIndex.genres.value: [
                genre_mock({
                    'id': '2f89e116-4827-4ff4-853c-b6e058f71e31',
                    'name': 'Action',
                }),
                
            ],
        },
        {
            'genre': '2f89e116-4827-4ff4-853c-b6e058f71e31',
            'page_size': 1,
            'page_number': 0,
        },
        {
            'status': HTTPStatus.UNPROCESSABLE_ENTITY,
            'data': {
                'detail': [
                    {
                        'type': 'greater_than_equal', 
                        'loc': ['query', 'page_number'], 
                        'msg': 'Input should be greater than or equal to 1',
                        'input': '0', 
                        'ctx': {'ge': 1}
                    }
                ]
            }
        }
    ],
])
@pytest.mark.asyncio()
async def test__get_films(
    clear_cache,
    fill_elastic_indices,
    make_get_request,
    preload_data,
    query_data,
    expected_answer
):
    await fill_elastic_indices(preload_data)
    
    response = await make_get_request("/api/v1/films/", query_data)
    assert response.status_code == expected_answer["status"]
    assert_have_json(
        should_be=expected_answer['data'],
        other=response.json(),
        exclude_ids=True
    )


@pytest.mark.parametrize('preload_data, query_data, expected_answer',[
    [
        {
            ESIndex.movies.value: [
                film_mock({
                    'title': 'Matrix',
                }),
                film_mock({
                    'title': 'Fight Club',
                }),
            ],
        },
        {},
        {
            'status': HTTPStatus.OK,
            'data': [
                response_film_mock({
                    'title': 'Matrix',
                }),
                response_film_mock({
                    'title': 'Fight Club',
                }),
            ]
        }
    ],
    [
        {
            ESIndex.movies.value: [],
        },
        {},
        {
            'status': HTTPStatus.OK,
            'data': [
                response_film_mock({
                    'title': 'Matrix',
                }),
                response_film_mock({
                    'title': 'Fight Club',
                }),
            ]
        }
    ],
])
@pytest.mark.asyncio()
async def test__get_films_cache(
    fill_elastic_indices,
    make_get_request,
    preload_data,
    query_data,
    expected_answer
):
    await fill_elastic_indices(preload_data)
    
    response = await make_get_request("/api/v1/films/", query_data)
    assert response.status_code == expected_answer["status"]
    assert_have_json(
        should_be=expected_answer['data'],
        other=response.json(),
        exclude_ids=True
    )