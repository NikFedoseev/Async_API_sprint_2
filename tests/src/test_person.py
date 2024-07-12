import pytest
from settings import ESIndex
from testdata.person_mocks import person_mock, person_film_mock, response_person_mock, response_person_film_mock
from utils.helpers import assert_have_json

@pytest.mark.parametrize("preload_data, query_data, expected_answer", [
    [
        {
            ESIndex.persons.value: [
                person_mock({
                    'full_name': 'Harrison Ford',
                }),
                person_mock({
                    'full_name': 'Chuck Norris',
                }),
            ],
        },
        {
            'name': 'Harrison Ford'
        },
        {
            'status': 200,
            'data': [
                response_person_mock({
                    'full_name': 'Harrison Ford',
                }),
            ]
        }
    ],
    [
        {
            ESIndex.persons.value: [
                person_mock({
                    'full_name': 'Harrison Ford',
                }),
                person_mock({
                    'full_name': 'Chuck Norris',
                }),
            ],
        },
        {
            'name': 'Robert De Niro'
        },
        {
            'status': 200,
            'data': []
        }
    ],
    [
        {
            ESIndex.persons.value: [
                person_mock({
                    'full_name': 'Harrison Ford',
                    'films': [
                        person_film_mock({
                            'roles': ['actor']
                        })
                    ]
                }),
                person_mock({
                    'full_name': 'Chuck Norris',
                    'films': [
                        person_film_mock({
                            'roles': ['writer']
                        })
                    ]
                }),
            ],
        },
        {
            'role': 'actor'
        },
        {
            'status': 200,
            'data': [
                response_person_mock({
                    'full_name': 'Harrison Ford',
                    'films': [
                        person_film_mock({
                            'roles': ['actor']
                        })
                    ]
                }),
            ]
        }
    ],
    [
        {
            ESIndex.persons.value: [
                person_mock({
                    'full_name': 'Harrison Ford',
                    'films': [
                        person_film_mock({
                            'title': '9 Muses of Star Empire',
                        })
                    ]
                }),
                person_mock({
                    'full_name': 'Chuck Norris',
                    'films': [
                        person_film_mock({
                            'title': 'Other folm',
                        })
                    ]
                }),
            ],
        },
        {
            'film_title': '9 Muses of Star Empire'
        },
        {
            'status': 200,
            'data': [
                response_person_mock({
                    'full_name': 'Harrison Ford',
                    'films': [
                        person_film_mock({
                            'title': '9 Muses of Star Empire',
                        })
                    ]
                }),
            ]
        }
    ],
    [
        {
            ESIndex.persons.value: [
                person_mock({
                    'full_name': 'Harrison Ford',
                }),
                person_mock({
                    'full_name': 'Chuck Norris',
                }),
            ],
        },
        {
            'film_title': 'Star',
            'page_number': -1
        },
        {
            'status': 422,
            'data': {'detail': [{'type': 'greater_than_equal', 'loc': ['query', 'page_number'], 'msg': 'Input should be greater than or equal to 1', 'input': '-1', 'ctx': {'ge': 1}}]}
        }
    ],
    [
        {
            ESIndex.persons.value: [
                person_mock({
                    'full_name': 'Harrison Ford',
                }),
                person_mock({
                    'full_name': 'Chuck Norris',
                }),
            ],
        },
        {},
        {
            'status': 400,
            'data': {'detail': 'query should contain at least one of filters: name, role, film_title'}
        }
    ],
])
@pytest.mark.asyncio()
async def test__search_persons(
    clear_cache,
    es_write_data,
    make_get_request,
    preload_data,
    query_data,
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
    
    response = await make_get_request("/api/v1/persons/search", query_data)
    assert response.status_code == expected_answer["status"]
    assert_have_json(
        should_be=expected_answer['data'],
        other=response.json(),
        exclude_ids=True
    )


@pytest.mark.parametrize('preload_data, person_id, expected_answer', [
    [
        {
            ESIndex.persons.value: [
                person_mock({'id': 'e52aada7-4377-4f08-a21a-033ce3f9f8ad'}),
                person_mock({'id': 'a6bbdf6c-8ea6-4978-82c5-2f7ad89046c7'}),
            ],
        },
        'e52aada7-4377-4f08-a21a-033ce3f9f8ad',
        {
            'status': 200,
            'data': response_person_mock({'id': 'e52aada7-4377-4f08-a21a-033ce3f9f8ad'}),
        }
    ],
    [
        {
            ESIndex.persons.value: [
                person_mock({'id': 'e52aada7-4377-4f08-a21a-033ce3f9f8ad'}),
                person_mock({'id': 'a6bbdf6c-8ea6-4978-82c5-2f7ad89046c7'}),
            ],
        },
        'f3062f15-c2c0-488e-b2ef-7f79e5d9078d',
        {
            'status': 404,
            'data': {'detail': 'Person not found'},
        }
    ],
    [
        {
            ESIndex.persons.value: [
                person_mock({'id': 'e52aada7-4377-4f08-a21a-033ce3f9f8ad'}),
                person_mock({'id': 'a6bbdf6c-8ea6-4978-82c5-2f7ad89046c7'}),
            ],
        },
        '123',
        {
            'status': 422,
            'data': {
                'detail': [
                    {
                        'type': 'uuid_parsing',
                        'loc': ['path', 'person_id'],
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
async def test__get_person_details(
    clear_cache,
    es_write_data,
    make_get_request,
    preload_data,
    person_id,
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
    
    response = await make_get_request(f"/api/v1/persons/{person_id}")
    assert response.status_code == expected_answer["status"]
    assert_have_json(
        should_be=expected_answer['data'],
        other=response.json(),
        exclude_ids=True
    )


@pytest.mark.parametrize('preload_data, person_id, expected_answer', [
    [
        {
            ESIndex.persons.value: [
                person_mock({
                    'id': 'e52aada7-4377-4f08-a21a-033ce3f9f8ad',
                    'films': [
                        person_film_mock({'title': 'Interstellar'}),
                        person_film_mock({'title': 'Fight Club'}),
                    ]
                }),
                person_mock({'id': 'a6bbdf6c-8ea6-4978-82c5-2f7ad89046c7'}),
            ],
        },
        'e52aada7-4377-4f08-a21a-033ce3f9f8ad',
        {
            'status': 200,
            'data': [
                response_person_film_mock({'title': 'Interstellar'}),
                response_person_film_mock({'title': 'Fight Club'}),
            ],
        }
    ],
    [
        {
            ESIndex.persons.value: [
                person_mock({
                    'id': 'e52aada7-4377-4f08-a21a-033ce3f9f8ad',
                    'films': [
                        person_film_mock({'title': 'Interstellar'}),
                        person_film_mock({'title': 'Fight Club'}),
                    ]
                }),
                person_mock({'id': 'a6bbdf6c-8ea6-4978-82c5-2f7ad89046c7'}),
            ],
        },
        'f3062f15-c2c0-488e-b2ef-7f79e5d9078d',
        {
            'status': 200,
            'data': [],
        }
    ],
     [
        {
            ESIndex.persons.value: [
                person_mock({
                    'id': 'e52aada7-4377-4f08-a21a-033ce3f9f8ad',
                    'films': [
                        person_film_mock({'title': 'Interstellar'}),
                        person_film_mock({'title': 'Fight Club'}),
                    ]
                }),
                person_mock({'id': 'a6bbdf6c-8ea6-4978-82c5-2f7ad89046c7'}),
            ],
        },
        '123',
        {
            'status': 422,
            'data': {
                'detail': [
                    {
                        'type': 'uuid_parsing',
                        'loc': ['path', 'person_id'],
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
async def test__get_person_films(
    clear_cache,
    es_write_data,
    make_get_request,
    preload_data,
    person_id,
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
    
    response = await make_get_request(f"/api/v1/persons/{person_id}/films")
    assert response.status_code == expected_answer["status"]
    assert_have_json(
        should_be=expected_answer['data'],
        other=response.json(),
        exclude_ids=True
    )