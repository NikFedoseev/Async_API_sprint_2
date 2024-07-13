import uuid

def person_film_mock(data = None):
    person_film = {
        'id': str(uuid.uuid4()),
        'title': '9 Muses of Star Empire',
        'imdb_rating': 9.0,
        'roles': ['actor']
    }
    person_film.update(data or {})
    return person_film


def response_person_film_mock(data = None):
    response_person_film = person_film_mock(data)
    del response_person_film['roles']
    return response_person_film


def person_mock(data = None):
    person = {
        'id': str(uuid.uuid4()),
        'full_name': 'Harrison Ford',
        'films': [person_film_mock()]
    }
    person.update(data or {})
    return person


def response_person_mock(data=None):
    response_person = person_mock(data)
    for film in response_person['films']:
        del film['title']
        del film['imdb_rating']

    return response_person