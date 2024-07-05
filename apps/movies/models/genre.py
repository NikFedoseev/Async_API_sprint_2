from uuid import UUID

from pydantic import BaseModel


class GenreFilmwork(BaseModel):
    id: UUID
    title: str
    imdb_rating: float | None


class Genre(BaseModel):
    id: UUID
    name: str
    description: str | None
    films: list[GenreFilmwork]
