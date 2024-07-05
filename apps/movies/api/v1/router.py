from api.v1.endpoints.film import router as film_router
from api.v1.endpoints.genre import router as genre_router
from api.v1.endpoints.person import router as person_router
from fastapi import APIRouter

api_router = APIRouter(prefix="/api/v1")


api_router.include_router(film_router, prefix="/films", tags=["Films"])
api_router.include_router(genre_router, prefix="/genres", tags=["Genres"])
api_router.include_router(person_router, prefix="/persons", tags=["Persons"])
