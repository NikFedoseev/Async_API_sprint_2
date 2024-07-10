from enum import StrEnum

from pydantic import Field
from pydantic_settings import BaseSettings


class ESIndex(StrEnum):
    movies = "movies"
    genres = "genres"
    persons = "persons"


class MyBaseSettings(BaseSettings):
    @property
    def url(self) -> str:
        return f"{self.host}:{self.port}"


class ElasticSettings(MyBaseSettings):
    host: str = Field("http://127.0.0.1")
    port: int = Field(9201)

    class Config:
        env_prefix = "ELASTIC_"


class RedisSettings(MyBaseSettings):
    host: str = Field("127.0.0.1")
    port: int = Field(6380)

    class Config:
        env_prefix = "REDIS_"


class PGSettings(MyBaseSettings):
    host: str = Field("127.0.0.1")
    port: int = Field(5433)

    class Config:
        env_prefix = "PG_"


class ServiceSettings(MyBaseSettings):
    host: str = Field("http://127.0.0.1")
    port: int = Field(8000)

    class Config:
        env_prefix = "SERVICE_"


class TestSettings(BaseSettings):
    es: ElasticSettings = ElasticSettings()  # type: ignore
    redis: RedisSettings = RedisSettings()  # type: ignore
    pg: PGSettings = PGSettings()  # type: ignore
    service: ServiceSettings = ServiceSettings()  # type: ignore


test_settings = TestSettings()
