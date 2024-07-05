from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv("../.env")


class PGSettings(BaseSettings):
    HOST: str
    PORT: str
    USER: str
    PASSWORD: str
    DB: str

    class Config:
        env_prefix = "POSTGRES_"


class ElasticSettings(BaseSettings):
    HOST: str
    PORT: str

    class Config:
        env_prefix = "ELASTIC_"


class ETLSettings(BaseSettings):
    START_TIME: str
    EXTRACT_SIZE: int
    CHECKING_UPDATES_SLEEP_TIME: float
    ITERATION_SLEEP_TIME: float
    STORAGE_FILE_PATH: str

    class Config:
        env_prefix = "ETL_"


class Settings(BaseSettings):
    pg: PGSettings = PGSettings()  # type: ignore
    elastic: ElasticSettings = ElasticSettings()  # type: ignore
    etl: ETLSettings = ETLSettings()  # type: ignore


settings = Settings()  # type: ignore
