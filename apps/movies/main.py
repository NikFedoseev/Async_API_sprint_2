from contextlib import asynccontextmanager

from api import api_router_v1
from db import elastic, redis
from elasticsearch import AsyncElasticsearch
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from redis.asyncio import Redis
from settings.api import api_settings
from settings.elastic import elastic_settings
from settings.redis import redis_settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis.redis = Redis.from_url(redis_settings.REDIS_URL)  # type: ignore[arg-type]
    elastic.es = AsyncElasticsearch(elastic_settings.ELASTIC_URL)
    yield
    await redis.redis.close()  # type: ignore[union-attr]
    await elastic.es.close()


app = FastAPI(
    title=api_settings.TITLE,
    openapi_url=api_settings.OPENAPI_URL,
    docs_url=api_settings.DOCS_URL,
    redoc_url=api_settings.REDOC_URL,
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
)


app.include_router(api_router_v1)
