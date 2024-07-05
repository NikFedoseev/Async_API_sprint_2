from settings.base import BaseSettings


class APISettings(BaseSettings):
    TITLE: str = "async-movies"
    OPENAPI_URL: str = "/api/v1/public/openapi.json"
    DOCS_URL: str = "/api/v1/public/docs"
    REDOC_URL: str = "/api/v1/public/redoc"

    LOG_QUERIES: bool = False


api_settings = APISettings()
