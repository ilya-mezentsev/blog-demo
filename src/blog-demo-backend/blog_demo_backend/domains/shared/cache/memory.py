from typing import (
    Dict,
    Any,
    Optional,
    Tuple,
)

import asyncio

from .base import ICache


__all__ = [
    'MemoryCacheRepository',
]


cache_lock = asyncio.Lock()


class MemoryCacheRepository(ICache):

    def __init__(self) -> None:

        self._cache: Dict[str, Any] = {}

    async def on_data_changed(self) -> None:
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
