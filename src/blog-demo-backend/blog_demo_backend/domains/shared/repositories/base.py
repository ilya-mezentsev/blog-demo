from abc import ABCMeta, abstractmethod
from typing import (
    TypeVar,
    Generic,
    Sequence,
)

from blog_demo_backend.domains.shared import Id


__all__ = [
    'IRepository',
]


T = TypeVar('T')


class IRepository(Generic[T], metaclass=ABCMeta):

    @abstractmethod
    async def create(self, model: T) -> None:
        raise NotImplementedError()

    # todo понять насчет фильтров поиска
    @abstractmethod
    async def read(self) -> Sequence[T]:
        raise NotImplementedError()

    @abstractmethod
    async def update(self, model: T) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def delete(self, model_id: Id) -> None:
        raise NotImplementedError()
