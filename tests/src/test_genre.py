import pytest
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
            'status': 200,
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
            'status': 404,
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
            'status': 422,
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
    es_write_data,
    make_get_request,
    preload_data,
    genre_id,
    expected_answer
):
    for name, data in preload_data.items():
        data_to_load = [
            {
                '_index': name,
                '_id': row['id'],
                '_source': row
            } 
            for row in data
        ]
        await es_write_data(name, data_to_load)
    
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
            'status': 200,
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
            'status': 200,
            'data': []
        }
    ],
])
@pytest.mark.asyncio()
async def test__get_genres(
    clear_cache,
    es_write_data,
    make_get_request,
    preload_data,
    expected_answer
):
    for name, data in preload_data.items():
        data_to_load = [
            {
                '_index': name,
                '_id': row['id'],
                '_source': row
            } 
            for row in data
        ]
        await es_write_data(name, data_to_load)
    
    response = await make_get_request("/api/v1/genres/")
    assert response.status_code == expected_answer["status"]
    assert_have_json(
        should_be=expected_answer['data'],
        other=response.json(),
        exclude_ids=True
    )