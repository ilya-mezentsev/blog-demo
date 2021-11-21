from abc import ABCMeta, abstractmethod
from typing import (
    Tuple,
    Optional,
    Any,
)


__all__ = [
    'ICache',
]


class ICache(metaclass=ABCMeta):

    @abstractmethod
    async def on_data_changed(self) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def reset_cache(self) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def get_cached(
            self,
            method: str,
            search: Optional[Any],
    ) -> Tuple[Optional[Any], bool]:
        """
        Возвращает кортеж, где
            * первый элемент - это значение из кеша, если есть
            * второй элемент - удалось ли это значение найти
        """

        raise NotImplementedError()

    @abstractmethod
    async def set_cached(
            self,
            method: str,
            search: Optional[Any],
            value: Any,
    ) -> None:

        raise NotImplementedError()
