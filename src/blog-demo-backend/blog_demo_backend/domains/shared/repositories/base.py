from abc import ABCMeta, abstractmethod
from typing import (
    TypeVar,
    Generic,
    Sequence,
    Optional,
)

from blog_demo_backend.domains.shared import Id


__all__ = [
    'IRepository',
]


ModelType = TypeVar('ModelType')
SpecificationType = TypeVar('SpecificationType')


class IRepository(
    Generic[
        ModelType,
        SpecificationType,
    ],
    metaclass=ABCMeta,
):

    @abstractmethod
    async def create(self, model: ModelType) -> None:
        raise NotImplementedError()

    async def read(
            self,
            specification: Optional[SpecificationType] = None,
    ) -> Sequence[ModelType]:

        if specification is not None:
            return await self._read(specification)

        else:
            return await self._read_all()

    @abstractmethod
    async def _read_all(self) -> Sequence[ModelType]:
        raise NotImplementedError()

    @abstractmethod
    async def _read(self, specification: SpecificationType) -> Sequence[ModelType]:
        raise NotImplementedError()

    @abstractmethod
    async def update(self, model: ModelType) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def delete(self, model_id: Id) -> None:
        raise NotImplementedError()
