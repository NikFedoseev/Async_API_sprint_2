from pydantic import Field
from pydantic_settings import BaseSettings
from utils.mapping import movie_index_config


class TestSettings(BaseSettings):
    es_host: str = Field("http://127.0.0.1:9201", env="ELASTIC_HOST")
    es_index: str = Field("movies", env="ELASTIC_INDEX")
    es_id_field: str = Field("wtf", env="ELASTIC_ID_FIELD")
    es_index_mapping: dict = Field(movie_index_config, env="ELASTIC_INDEX_MAPPING")

    redis_host: str = Field("http://127.0.0.1:6380", env="REDIS_HOST")
    service_url: str = Field("http://127.0.0.1:8000", env="SERVICE_URL")


test_settings = TestSettings()
