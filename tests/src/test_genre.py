import pytest
from http import HTTPStatus
from settings import ESIndex
from testdata.genre_mocks import genre_mock, response_genre_mock
from utils.helpers import assert_have_json


@pytest.mark.parametrize("preload_data, genre_id, expected_answer", [
    [
        {
            ESIndex.genres.value: [
                genre_mock({
                    'id': '3d8d9bf5-0d90-4353-88ba-4ccc5d2c07ff',
                    'name': 'Adventure',
                }),
                genre_mock({
                    'id': '120a21cf-9097-479e-904a-13dd7198c1dd',
                    'name': 'Fantasy',
                }),
            ],
        },
       '3d8d9bf5-0d90-4353-88ba-4ccc5d2c07ff',
        {
            'status': HTTPStatus.OK,
            'data': response_genre_mock({
                'id': '3d8d9bf5-0d90-4353-88ba-4ccc5d2c07ff',
                'name': 'Adventure',
            }),
        }
    ],
    [
        {
            ESIndex.genres.value: [
                genre_mock({
                    'id': '3d8d9bf5-0d90-4353-88ba-4ccc5d2c07ff',
                    'name': 'Fantasy',
                }),
            ],
        },
       'ae90bcce-aa4d-426c-8be4-b1b61b7f186a',
        {
            'status': HTTPStatus.NOT_FOUND,
            'data': {'detail': 'Genre not found'}
        }
    ],
    [
        {
            ESIndex.genres.value: [
                genre_mock({
                    'id': '3d8d9bf5-0d90-4353-88ba-4ccc5d2c07ff',
                    'name': 'Fantasy',
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
                        'loc': ['path', 'genre_id'],
                        'msg': 'Input should be a valid UUID, invalid length: expected length 32 for simple format, found 3',
                        'input': '123',
                        'ctx': {'error': 'invalid length: expected length 32 for simple format, found 3'}
                    }
                ]
            }
        }
    ],
])
@pytest.mark.asyncio()
async def test__get_genre_by_id(
    clear_cache,
    fill_elastic_indices,
    make_get_request,
    preload_data,
    genre_id,
    expected_answer
):
    await fill_elastic_indices(preload_data)
    
    response = await make_get_request(f"/api/v1/genres/{genre_id}")
    assert response.status_code == expected_answer["status"]
    assert_have_json(
        should_be=expected_answer['data'],
        other=response.json(),
        exclude_ids=True
    )


@pytest.mark.parametrize("preload_data, genre_id, expected_answer", [
    [
        {
            ESIndex.genres.value: [
                genre_mock({
                    'id': '3d8d9bf5-0d90-4353-88ba-4ccc5d2c07ff',
                    'name': 'Adventure',
                }),
                genre_mock({
                    'id': '120a21cf-9097-479e-904a-13dd7198c1dd',
                    'name': 'Fantasy',
                }),
            ],
        },
       '3d8d9bf5-0d90-4353-88ba-4ccc5d2c07ff',
        {
            'status': HTTPStatus.OK,
            'data': response_genre_mock({
                'id': '3d8d9bf5-0d90-4353-88ba-4ccc5d2c07ff',
                'name': 'Adventure',
            }),
        }
    ],
    [
        {
            ESIndex.genres.value: [],
        },
       '3d8d9bf5-0d90-4353-88ba-4ccc5d2c07ff',
        {
            'status': HTTPStatus.OK,
            'data': response_genre_mock({
                'id': '3d8d9bf5-0d90-4353-88ba-4ccc5d2c07ff',
                'name': 'Adventure',
            }),
        }
    ],
])
@pytest.mark.asyncio()
async def test__get_genre_by_id_cache(
    fill_elastic_indices,
    make_get_request,
    preload_data,
    genre_id,
    expected_answer
):
    await fill_elastic_indices(preload_data)
    
    response = await make_get_request(f"/api/v1/genres/{genre_id}")
    assert response.status_code == expected_answer["status"]
    assert_have_json(
        should_be=expected_answer['data'],
        other=response.json(),
        exclude_ids=True
    )


@pytest.mark.parametrize("preload_data, expected_answer", [
    [
        {
            ESIndex.genres.value: [
                genre_mock({
                    'id': '3d8d9bf5-0d90-4353-88ba-4ccc5d2c07ff',
                    'name': 'Adventure',
                }),
                genre_mock({
                    'id': '120a21cf-9097-479e-904a-13dd7198c1dd',
                    'name': 'Fantasy',
                }),
            ],
        },
        {
            'status': HTTPStatus.OK,
            'data': [
                response_genre_mock({
                    'id': '3d8d9bf5-0d90-4353-88ba-4ccc5d2c07ff',
                    'name': 'Adventure',
                }),
                response_genre_mock({
                    'id': '120a21cf-9097-479e-904a-13dd7198c1dd',
                    'name': 'Fantasy',
                }),
            ]
        }
    ],
    [
        {
            ESIndex.genres.value: [],
        },
        {
            'status': HTTPStatus.OK,
            'data': []
        }
    ],
])
@pytest.mark.asyncio()
async def test__get_genres(
    clear_cache,
    fill_elastic_indices,
    make_get_request,
    preload_data,
    expected_answer
):
    await fill_elastic_indices(preload_data)
    
    response = await make_get_request("/api/v1/genres/")
    assert response.status_code == expected_answer["status"]
    assert_have_json(
        should_be=expected_answer['data'],
        other=response.json(),
        exclude_ids=True
    )


@pytest.mark.parametrize("preload_data, expected_answer", [
    [
        {
            ESIndex.genres.value: [
                genre_mock({
                    'id': '3d8d9bf5-0d90-4353-88ba-4ccc5d2c07ff',
                    'name': 'Adventure',
                }),
                genre_mock({
                    'id': '120a21cf-9097-479e-904a-13dd7198c1dd',
                    'name': 'Fantasy',
                }),
            ],
        },
        {
            'status': HTTPStatus.OK,
            'data': [
                response_genre_mock({
                    'id': '3d8d9bf5-0d90-4353-88ba-4ccc5d2c07ff',
                    'name': 'Adventure',
                }),
                response_genre_mock({
                    'id': '120a21cf-9097-479e-904a-13dd7198c1dd',
                    'name': 'Fantasy',
                }),
            ]
        }
    ],
    [
        {
            ESIndex.genres.value: [],
        },
        {
            'status': HTTPStatus.OK,
            'data': [
                response_genre_mock({
                    'id': '3d8d9bf5-0d90-4353-88ba-4ccc5d2c07ff',
                    'name': 'Adventure',
                }),
                response_genre_mock({
                    'id': '120a21cf-9097-479e-904a-13dd7198c1dd',
                    'name': 'Fantasy',
                }),
            ]
        }
    ],
])
@pytest.mark.asyncio()
async def test__get_genres_cache(
    fill_elastic_indices,
    make_get_request,
    preload_data,
    expected_answer
):
    await fill_elastic_indices(preload_data)
    
    response = await make_get_request("/api/v1/genres/")
    assert response.status_code == expected_answer["status"]
    assert_have_json(
        should_be=expected_answer['data'],
        other=response.json(),
        exclude_ids=True
    )