from uuid import UUID

from api.deps import FilmService
from api.v1.schemas.film import DetailedFilmSchema, FilmSchema
from fastapi import APIRouter, HTTPException, status

router = APIRouter()


@router.get("/search", response_model=list[FilmSchema])
async def search_films(
    film_service: FilmService,
    title: str,
    page_size: int = 20,
    page_number: int = 1,
):
    """
    Поиск фильмов по названию
    """
    films = await film_service.search(title=title, page_size=page_size, page_number=page_number)
    return films


@router.get("/{film_id}", response_model=DetailedFilmSchema)
async def film_details(film_id: UUID, film_service: FilmService):
    """
    Получить информацию о фильме по идентификатору
    """
    film = await film_service.get_by_id(film_id)

    if not film:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Film not found")

    return film


@router.get("/", response_model=list[FilmSchema])
async def get_films(
    film_service: FilmService,
    sort: str | None = None,
    genre: UUID | None = None,
    page_size: int = 20,
    page_number: int = 1,
):
    """
    Получить список фильмов для вывода на главную страницу
    """
    films = await film_service.get_all(sort=sort, genre_id=str(genre), page_size=page_size, page_number=page_number)
    return films
