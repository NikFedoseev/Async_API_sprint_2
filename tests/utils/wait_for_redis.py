import logging
import time

import backoff
from redis import Redis

from settings import test_settings


def handle_backoff(details):
    logging.error("Backing off {wait:0.1f} seconds after {tries} tries. Calling function {targer}".format(**details))


@backoff.on_exception(
    backoff.expo,
    (ConnectionError,),
    on_backoff=handle_backoff,
)
def setup_redis_connection():
    redis_client = Redis(host=test_settings.redis.host, port=test_settings.redis.port)
    if not redis_client.ping():
        raise ConnectionError("Could not connect to redis")
    return redis_client


if __name__ == "__main__":
    redis_client = setup_redis_connection()
