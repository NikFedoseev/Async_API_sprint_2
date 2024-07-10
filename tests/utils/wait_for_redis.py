import time

from redis import Redis

from settings import test_settings

if __name__ == "__main__":
    redis_client = Redis(host=test_settings.redis.host, port=test_settings.redis.port)
    while True:
        if redis_client.ping():
            break
        time.sleep(1)
