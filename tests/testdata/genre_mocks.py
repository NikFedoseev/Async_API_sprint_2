import uuid


def genre_film_mock(data=None):
    genre_film = {
        "id": str(uuid.uuid4()),
        "title": "Fight Club",
        "imdb_rating": 9.0,
    }
    genre_film.update(data or {})
    return genre_film


def genre_mock(data=None):
    genre = {"id": str(uuid.uuid4()), "name": "Adventure", "description": None, "films": [genre_film_mock()]}
    genre.update(data or {})
    return genre


def response_genre_mock(data=None):
    response_genre = genre_mock(data)
    del response_genre["description"]
    del response_genre["films"]
    return response_genre
