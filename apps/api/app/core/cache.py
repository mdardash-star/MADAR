from redis import Redis

from app.core.config import settings

redis_client = Redis(
    host=settings.redis_host,
    port=settings.redis_port,
    decode_responses=True,
    socket_connect_timeout=2,
)


def set_cache_value(key: str, value: str, ttl_seconds: int = 3600) -> None:
    redis_client.setex(key, ttl_seconds, value)


def get_cache_value(key: str) -> str | None:
    return redis_client.get(key)
