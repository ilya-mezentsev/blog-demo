from typing import (
    Optional,
    Any,
    Tuple,
)

from .base import ICache


__all__ = [
    'CacheMiss',
]


class CacheMiss(ICache):
    """
    Класс для имитации всегда пустого кеша
    """

    async def on_data_changed(self) -> None:
        pass

    async def reset_cache(self) -> None:
        pass

    async def get_cached(self, method: str, search: Optional[Any]) -> Tuple[Optional[Any], bool]:
        return None, False

    async def set_cached(self, method: str, search: Optional[Any], value: Any) -> None:
        pass
