from pathlib import Path

from pydantic_settings import BaseSettings as PydanticBaseSettings
from pydantic_settings import SettingsConfigDict

ROOT_DIR = Path(__file__).resolve(strict=True).parent.parent.parent


class BaseSettings(PydanticBaseSettings):
    model_config = SettingsConfigDict(env_file=ROOT_DIR.joinpath(".env"), case_sensitive=True, extra="allow")
