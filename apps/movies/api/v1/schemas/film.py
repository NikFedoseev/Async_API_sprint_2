from uuid import UUID

from api.v1.schemas.base import BaseSchema


class FilmPerson(BaseSchema):
    id: UUID
    name: str


class FilmSchema(BaseSchema):
    id: UUID
    imdb_rating: float | None
    title: str


class DetailedFilmSchema(BaseSchema):
    id: UUID
    imdb_rating: float | None
    title: str
    description: str | None
    genres: list[str]
    directors_names: list[str]
    actors_names: list[str]
    writers_names: list[str]
    directors: list[FilmPerson]
    actors: list[FilmPerson]
    writers: list[FilmPerson]
