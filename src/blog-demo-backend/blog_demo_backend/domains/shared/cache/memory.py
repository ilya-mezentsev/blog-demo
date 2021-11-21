from typing import (
    Dict,
    Any,
    Optional,
    Tuple,
    Callable,
)

import asyncio
import aioredis

from .base import ICache


__all__ = [
    'MemoryCache',
    'CacheFactoryFn',
]

CacheFactoryFn = Callable[[str], 'ICache']

cache_lock = asyncio.Lock()


class MemoryCache(ICache):

    def __init__(
            self,
            reset_cache_channel: str,
            entity_type: str,
            redis: aioredis.Redis
    ) -> None:

        self._reset_cache_channel = reset_cache_channel
        self._entity_type = entity_type
        self._redis = redis
        self._cache: Dict[str, Any] = {}

    async def on_data_changed(self) -> None:
        # Нода, которая отправляет это сообщение, тоже его получит =>
        # тут не нужно вызывать self.reset_cache
        await self._redis.publish(
            channel=self._reset_cache_channel,
            message=self._entity_type,
        )

    async def reset_cache(self) -> None:
        async with cache_lock:
            self._cache.clear()

    async def get_cached(
            self,
            method: str,
            search: Optional[Any],
    ) -> Tuple[Optional[Any], bool]:

        key = self._make_key(method, search)

        async with cache_lock:
            if key in self._cache:
                return self._cache[key], True
            else:
                return None, False

    async def set_cached(
            self,
            method: str,
            search: Optional[Any],
            value: Any,
    ) -> None:

        key = self._make_key(method, search)

        async with cache_lock:
            self._cache[key] = value

    def _make_key(
            self,
            method: str,
            search: Optional[Any],
    ) -> str:

        return f'{self.__class__.__name__}.{method}({search!s})'
