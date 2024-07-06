from typing import Annotated

from fastapi import Depends, Query

from services.film import FilmService as _FilmService
from services.film import get_film_service
from services.genre import GenreService as _GenreService
from services.genre import get_genre_service
from services.person import PersonService as _PersonService
from services.person import get_person_service

FilmService = Annotated[_FilmService, Depends(get_film_service)]
GenreService = Annotated[_GenreService, Depends(get_genre_service)]
PersonService = Annotated[_PersonService, Depends(get_person_service)]


class PaginateQueryParams:
    def __init__(
        self,
        page_number: int = Query(
            1,
            title="Page number.",
            description="Page number to return",
            ge=1,
        ),
        page_size: int = Query(
            50,
            title="Size of page.",
            description="The number of records returned per page",
            ge=1,
            le=500,
        ),
    ):
        self.page_number = page_number
        self.page_size = page_size
