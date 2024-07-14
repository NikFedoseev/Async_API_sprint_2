import pytest_asyncio
from redis import Redis

from settings import test_settings


@pytest_asyncio.fixture(scope="session")
def redis_client():
    redis = Redis.from_url(test_settings.redis.url)
    yield redis
    redis.close()


@pytest_asyncio.fixture()
def clear_cache(redis_client):
    redis_client.flushdb()
    yield
