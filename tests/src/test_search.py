import pytest
from settings import ESIndex
from testdata.person_mocks import person_mock, person_film_mock, response_person_mock
from tests.testdata.film_mocks import film_mock, response_film_mock
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
                            'roles': ['actor']
                        })
                    ]
                }),
            ],
        },
        {
            'role': 'actor',
            'page_size': 1,
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
])
@pytest.mark.asyncio()
async def test__search_persons(
    clear_cache,
    fill_elastic_indices,
    make_get_request,
    preload_data,
    query_data,
    expected_answer
):
   
    await fill_elastic_indices(preload_data)
    
    response = await make_get_request("/api/v1/persons/search", query_data)
    assert response.status_code == expected_answer["status"]
    assert_have_json(
        should_be=expected_answer['data'],
        other=response.json(),
        exclude_ids=True
    )


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
            ESIndex.persons.value: [],
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
])
@pytest.mark.asyncio()
async def test__search_persons_cache(
    fill_elastic_indices,
    make_get_request,
    preload_data,
    query_data,
    expected_answer
):
    await fill_elastic_indices(preload_data)
    
    response = await make_get_request("/api/v1/persons/search", query_data)
    assert response.status_code == expected_answer["status"]
    assert_have_json(
        should_be=expected_answer['data'],
        other=response.json(),
        exclude_ids=True
    )


@pytest.mark.parametrize("preload_data, query_data, expected_answer", [
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
        {
            'title': 'Matrix'
        },
        {
            'status': 200,
            'data': [
                response_film_mock({
                    'title': 'Matrix',
                })
            ]
        }
    ],
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
        {
            'title': 'sdmfklmdsflk'
        },
        {
            'status': 200,
            'data': []
        }
    ],
    [
        {
            ESIndex.movies.value: [
                film_mock({
                    'title': 'Matrix',
                }),
                film_mock({
                    'title': 'Fight Club',
                }),
                film_mock({
                    'title': 'Star Wars: Episode IV - A New Hope',
                }),
                film_mock({
                    'title': 'Star Wars: Episode VI - Return of the Jedi',
                }),
                film_mock({
                    'title': 'Star Wars: Episode V - The Empire Strikes Back',
                }),
            ],
        },
        {
            'title': 'Star Wars',
            'page_size': 2,
        },
        {
            'status': 200,
            'data': [
                response_film_mock({
                    'title': 'Star Wars: Episode IV - A New Hope',
                }),
                response_film_mock({
                    'title': 'Star Wars: Episode VI - Return of the Jedi',
                }),
            ]
        }
    ],
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
        {
            'page_size': -1,
        },
        {
            'status': 422,
            'data': {
                'detail': [
                    {
                        'type': 'greater_than_equal', 
                        'loc': ['query', 'page_size'], 
                        'msg': 'Input should be greater than or equal to 1', 
                        'input': '-1', 
                        'ctx': {'ge': 1}
                    }, 
                    {
                        'type': 'missing', 
                        'loc': ['query', 'title'], 
                        'msg': 'Field required', 
                        'input': None
                    }
                ]
            }
        }
    ],
])
@pytest.mark.asyncio()
async def test__search_films(
    clear_cache,
    fill_elastic_indices,
    make_get_request,
    preload_data,
    query_data,
    expected_answer
):
    await fill_elastic_indices(preload_data)
    
    response = await make_get_request("/api/v1/films/search", query_data)
    assert response.status_code == expected_answer["status"]
    assert_have_json(
        should_be=expected_answer['data'],
        other=response.json(),
        exclude_ids=True
    )


@pytest.mark.parametrize("preload_data, query_data, expected_answer", [
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
        {
            'title': 'Matrix'
        },
        {
            'status': 200,
            'data': [
                response_film_mock({
                    'title': 'Matrix',
                })
            ]
        }
    ],
    [
        {
            ESIndex.movies.value: [],
        },
        {
            'title': 'Matrix'
        },
        {
            'status': 200,
            'data': [
                response_film_mock({
                    'title': 'Matrix',
                })
            ]
        }
    ],
])
@pytest.mark.asyncio()
async def test__search_films_cache(
    fill_elastic_indices,
    make_get_request,
    preload_data,
    query_data,
    expected_answer
):
    await fill_elastic_indices(preload_data)
    
    response = await make_get_request("/api/v1/films/search", query_data)
    assert response.status_code == expected_answer["status"]
    assert_have_json(
        should_be=expected_answer['data'],
        other=response.json(),
        exclude_ids=True
    )