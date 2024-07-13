import uuid


def film_person_mock(data = None):
    film_person = {
        'id': str(uuid.uuid4()),
        'name': 'Keanu Reeves'
    }
    film_person.update(data or {})
    return film_person


def film_mock(data = None):
    film = {
        'id': str(uuid.uuid4()),
        'imdb_rating': 9.0,
        'title': 'Matrix',
        'description': 'Wake up, Neo',
        'genres': ['Action'],
        'directors_names': [
            'Lana Wachowski',
            'Lilly Wachowski'
        ],
        'actors_names': [
            'Keanu Reeves',
        ],
        'writers_names': [
            'Lana Wachowski',
            'Lilly Wachowski'
        ],
        'directors': [
            film_person_mock({'name': 'Lana Wachowski'}),
            film_person_mock({'name': 'Lilly Wachowski'}),
        ],
        'actors': [
            film_person_mock({'name': 'Keanu Reeves'}),
        ],
        'writers': [
            film_person_mock({'name': 'Lana Wachowski'}),
            film_person_mock({'name': 'Lilly Wachowski'}),
        ],
    }
    film.update(data or {})
    return film


def response_detailed_film_mock(data = None):
    response_detailed_film = film_mock(data)
    return response_detailed_film


def response_film_mock(data = None):
    response_film = {
        'id': str(uuid.uuid4()),
        'imdb_rating': 9.0,
        'title': 'Matrix'
    }
    response_film.update(data or {})
    return response_film