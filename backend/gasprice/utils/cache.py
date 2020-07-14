"""Cache module
"""
import json
import redis
import logging

from json import JSONEncoder
from typing import Any, Callable
from functools import wraps

from gasprice import config


logger = logging.getLogger(__name__)


# Singleton
cache_client = None


def get_cache_client():
    """Create cache client (redis) base on setting
    """
    global cache_client
    if not cache_client:
        if config.TESTING:
            import fakeredis
            cache_client = fakeredis.FakeStrictRedis()
        else:
            cache_client = redis.from_url(config.REDIS_URL)
    return cache_client


def keysify(*args, sparator: str = '_') -> str:
    """Turn list of args in to cache key
    """
    return sparator.join(map(str, args))


def _should_cache_not_None(ret: Any) -> bool:
    return ret is not None


def should_cache_api_response(ret) -> bool:
    """Should cache function for 3rd party api response

    3rd api response must have return type of tuple
    (result, status_code, headers)

    Returns:
        True if status_code == 200
    """
    _, status_code, _ = ret
    return status_code == 200


def make_key_from_args(*args, **kwargs) -> str:
    """Make cache key from args, combine all string
    """
    key_args = ','.join(map(str, args))
    key_kwargs = ','.join(f'{k}={v}' for k, v in kwargs.items())
    return f'({key_args},{key_kwargs})'


def cached(
        static_key: str = None,
        make_key: Callable = None,
        expire: int = config.CACHE_DEFAULT_EXPIRED,
        prefix: str = config.CACHE_PREFIX,
        suffix: str = '',
        should_cache: Callable = None,
        encoder: json.JSONEncoder = None
) -> Callable:
    """Cached decorator factory

    Args:
        static_key: static key will be use for cache
        make_key: function to make cache key, function will be call with
                  *args and **kwargs. Ignore if statickey present
        expire: set cache expire, number of seconds
        prefix: prepend prefix to cache key
        suffix: append suffix to cache key
        should_cache: call back to decide should cache result or not,
                      default cache everything evaluated to True
        encoder: Json encoder instance

    Returns:
        Cached wrapper
    """
    if should_cache is None:
        should_cache = _should_cache_not_None

    cache_client = get_cache_client()

    def cache_outer(fn: Callable):
        fn_name = fn.__name__

        @wraps(fn)
        def cache_inner(*args, **kwargs):
            if static_key is not None:
                key = static_key
            else:
                key = make_key(*args, **kwargs)
            cache_key = keysify(prefix, fn_name, key, suffix)

            try:
                from_cache = cache_client.get(cache_key)
                if from_cache is not None:
                    logger.debug(f'Cache hit {cache_key}')
                    return json.loads(from_cache)
            except json.JSONDecodeError as ex:
                logger.error(f'cache decode error for key "{cache_key}", {ex}')

            result = fn(*args, **kwargs)
            try:
                if should_cache(result):
                    logger.debug(f'Cache set {cache_key}')
                    cache_client.set(
                        cache_key, json.dumps(result, cls=encoder))

                    if expire:
                        cache_client.expire(cache_key, expire)
            except Exception as ex:
                logger.error(f'cache save failed key for "{cache_key}". {ex}')

            return result

        return cache_inner

    return cache_outer


class Cache:
    def __init__(self):
        pass

    def set(self, key: str, value: str):
        """Set cache value

        Silently fail if cannot set value
        """
        pass

    def get(self, key: str, default=None):
        """Try to get key from cache

        Return default value if not found
        """
        pass

    def set_json(self, key: str, value: Any, encoder: JSONEncoder = None):
        """Set json value to cache
        """
        jsonstr = json.dumps(value, cls=encoder)
        self.set(key, jsonstr)

    def get_json(self, key: str, default=None):
        """Get json value from cache
        """
        cached = self.get(key)
        if cached is not None:
            try:
                return json.loads(cached)
            except ValueError:
                pass
        return default
