import redis
import os

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

redis_client = redis.from_url(REDIS_URL, decode_responses=True)

AUTHENTICATED_LIMIT = 10
ANONYMOUS_LIMIT = 2
WINDOW_SECONDS = 60


def is_rate_limited(identifier: str, is_authenticated: bool) -> bool:
    limit = AUTHENTICATED_LIMIT if is_authenticated else ANONYMOUS_LIMIT
    key = f"rate_limit:{identifier}"

    current = redis_client.get(key)

    if current is None:
        redis_client.setex(key, WINDOW_SECONDS, 1)
        return False

    if int(current) >= limit:
        return True

    redis_client.incr(key)
    return False
