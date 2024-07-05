from typing import Annotated

from db.elastic import get_elastic
from db.redis import get_redis
from elasticsearch import AsyncElasticsearch
from fastapi import Depends
from redis.asyncio import Redis

ElasticClient = Annotated[AsyncElasticsearch, Depends(get_elastic)]
RedisClient = Annotated[Redis, Depends(get_redis)]
