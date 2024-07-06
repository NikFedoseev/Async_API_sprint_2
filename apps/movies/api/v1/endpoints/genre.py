from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from api.deps import GenreService
from api.v1.schemas.genre import GenreSchema
from models import Genre

router = APIRouter()


@router.get("/{genre_id}", response_model=GenreSchema)
async def genre_by_id(genre_id: UUID, genre_service: GenreService) -> Genre:
    genre = await genre_service.get_by_id(genre_id)

    if not genre:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Genre not found")

    return genre


@router.get("/", response_model=list[GenreSchema])
async def genre_list(genre_service: GenreService) -> list[Genre]:
    genres = await genre_service.get_all_genres()

    return genres
