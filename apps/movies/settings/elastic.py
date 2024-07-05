from pydantic import HttpUrl, field_validator
from pydantic_core.core_schema import FieldValidationInfo
from settings.base import BaseSettings


class ElasticSettings(BaseSettings):
    ELASTIC_HOST: str
    ELASTIC_PORT: int
    ELASTIC_URL: str | None = None

    @field_validator("ELASTIC_URL", mode="before")
    @classmethod
    def assemble_elasticsearch_url(cls, v: str | None, info: FieldValidationInfo) -> str:
        if isinstance(v, str):
            return v

        scheme = "http"
        host = info.data["ELASTIC_HOST"]
        port = info.data["ELASTIC_PORT"]

        url = f"{scheme}://{host}:{port}"
        return HttpUrl(url).unicode_string()


elastic_settings = ElasticSettings()  # type: ignore[call-arg]
