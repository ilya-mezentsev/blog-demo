from abc import ABCMeta, abstractmethod
from typing import (
    TypeVar,
    Generic,
    Sequence,
    Optional,
    Union,
)

from ..types import Id


__all__ = [
    'ICreator',
    'IReader',
    'IUpdater',
    'IDeleter',
    'IRepository',
]


ModelType = TypeVar('ModelType')
SpecificationType = TypeVar('SpecificationType')


class ICreator(Generic[ModelType], metaclass=ABCMeta):
    @abstractmethod
    async def create(self, model: ModelType) -> None:
        raise NotImplementedError()


class IReader(
    Generic[
        ModelType,
        SpecificationType,
    ],
    metaclass=ABCMeta,
):
    async def read(
            self,
            specification: Optional[SpecificationType] = None,
    ) -> Union[
        Sequence[ModelType],
        Optional[ModelType],
    ]:

        if specification is not None:
            return await self._read(specification)

        else:
            return await self._read_all()

    @abstractmethod
    async def _read_all(self) -> Sequence[ModelType]:
        raise NotImplementedError()

    @abstractmethod
    async def _read(self, specification: SpecificationType) -> Optional[ModelType]:
        raise NotImplementedError()


class IUpdater(Generic[ModelType], metaclass=ABCMeta):
    @abstractmethod
    async def update(self, model: ModelType) -> None:
        raise NotImplementedError()


class IDeleter(Generic[ModelType], metaclass=ABCMeta):
    @abstractmethod
    async def delete(self, model_id: Id) -> None:
        raise NotImplementedError()


class IRepository(
    ICreator[ModelType],
    IReader[ModelType, SpecificationType],
    IUpdater[ModelType],
    IDeleter[ModelType],
    metaclass=ABCMeta,
):
    pass
