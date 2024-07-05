from uuid import UUID

from api.v1.schemas.base import BaseSchema


class GenreSchema(BaseSchema):
    id: UUID
    name: str
