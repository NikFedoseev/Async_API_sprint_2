from uuid import UUID

from api.deps import PersonService
from api.v1.schemas.film import FilmSchema
from api.v1.schemas.person import PersonSchema
from fastapi import APIRouter, HTTPException, status

router = APIRouter()


@router.get("/search")
async def search(
    person_service: PersonService,
    name: str | None = None,
    role: str | None = None,
    film_title: str | None = None,
    page_size: int = 20,
    page_number: int = 1,
) -> list[PersonSchema]:
    """
    Поиск персон по имени, роли и названию фильма
    """

    return await person_service.search(page_size, page_number, name, role, film_title)


@router.get("/{person_id}")
async def details(person_service: PersonService, person_id: UUID) -> PersonSchema:
    """
    Получить информацию о персоне по идентификатору
    """

    person = await person_service.get_by_id(person_id)

    if not person:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Person not found")

    return person


@router.get("/{person_id}/films")
async def films(
    person_service: PersonService,
    person_id: UUID,
    page_size: int = 20,
    page_number: int = 1,
) -> list[FilmSchema]:
    """
    Список фильмов персоны
    """

    return await person_service.get_films(person_id, page_size, page_number)
