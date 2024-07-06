from typing import Annotated

from elasticsearch import AsyncElasticsearch
from fastapi import Depends
from redis.asyncio import Redis

from db.elastic import get_elastic
from db.redis import get_redis

ElasticClient = Annotated[AsyncElasticsearch, Depends(get_elastic)]
RedisClient = Annotated[Redis, Depends(get_redis)]
