from enum import StrEnum

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class ESIndex(StrEnum):
    movies = "movies"
    genres = "genres"
    persons = "persons"


class MyBaseSettings(BaseSettings):
    @property
    def url(self) -> str:
        return f"http://{self.host}:{self.port}"


class ElasticSettings(MyBaseSettings):
    host: str = Field("127.0.0.1")
    port: int = Field(9201)

    model_config = SettingsConfigDict(env_prefix="ELASTIC_")


class RedisSettings(MyBaseSettings):
    host: str = Field("redis://127.0.0.1")
    port: int = Field(6380)
    db: int = Field(0)

    @property
    def url(self) -> str:
        return f"redis://{self.host}:{self.port}"

    model_config = SettingsConfigDict(env_prefix="REDIS_")


class ServiceSettings(MyBaseSettings):
    host: str = Field("127.0.0.1")
    port: int = Field(8000)

    model_config = SettingsConfigDict(env_prefix="SERVICE_")


class TestSettings(BaseSettings):
    es: ElasticSettings = ElasticSettings()  # type: ignore
    redis: RedisSettings = RedisSettings()  # type: ignore
    service: ServiceSettings = ServiceSettings()  # type: ignore


test_settings = TestSettings()
