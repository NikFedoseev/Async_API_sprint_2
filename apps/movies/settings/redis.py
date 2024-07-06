from pydantic import RedisDsn, field_validator
from pydantic_core.core_schema import FieldValidationInfo

from settings.base import BaseSettings


class RedisSettings(BaseSettings):
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_DB: int
    REDIS_URL: str | None = None

    @field_validator("REDIS_URL", mode="before")
    @classmethod
    def assemble_redis_url(cls, v: str | None, info: FieldValidationInfo) -> str:
        if isinstance(v, str):
            return v

        scheme = "redis"
        host = info.data["REDIS_HOST"]
        port = info.data["REDIS_PORT"]
        db = info.data["REDIS_DB"]

        url = f"{scheme}://{host}:{port}/{db}"
        return RedisDsn(url).unicode_string()


redis_settings = RedisSettings()  # type: ignore[call-arg]
