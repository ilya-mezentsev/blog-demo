from abc import ABCMeta, abstractmethod
from typing import (
    TypeVar,
    Generic,
    Sequence,
    Optional,
    Mapping,
    Any,
)

import sqlalchemy as sa  # type: ignore

from blog_demo_backend.shared import DBConnectionFn

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


class IRepositoryMixin:
    @property
    @abstractmethod
    def _table(self) -> sa.Table:
        raise NotImplementedError()

    @property
    @abstractmethod
    def _connect(self) -> DBConnectionFn:
        raise NotImplementedError()


class ICreator(
    Generic[ModelType],
    IRepositoryMixin,
    metaclass=ABCMeta,
):
    async def create(self, model: ModelType) -> None:
        query = self._table. \
            insert(). \
            values(self._make_create_mapping(model))

        async with self._connect() as conn:
            await conn.execute(query)

    @abstractmethod
    def _make_create_mapping(self, model: ModelType) -> Mapping[sa.Column, Any]:
        raise NotImplementedError()


class IReader(
    Generic[
        ModelType,
        SpecificationType,
    ],
    IRepositoryMixin,
    metaclass=ABCMeta,
):

    async def read_one(self, specification: SpecificationType) -> Optional[ModelType]:

        query = self._table. \
            select(). \
            where(self._make_where_for_read(specification))

        async with self._connect() as conn:
            row_result = await conn.execute(query)
            row = row_result.fetchone()

        if row:
            return self._model_from_row(row)
        else:
            return None

    async def read_all(
            self,
            specification: Optional[SpecificationType] = None,
    ) -> Sequence[ModelType]:

        query = self._table.select()
        if specification is not None:
            query = query.where(self._make_where_for_read(specification))

        async with self._connect() as conn:
            rows_result = await conn.execute(query)
            rows = rows_result.fetchall()

        return list(map(self._model_from_row, rows))

    @abstractmethod
    def _make_where_for_read(self, specification: SpecificationType) -> sa.sql.ColumnElement:
        raise NotImplementedError()

    @abstractmethod
    def _model_from_row(self, model_row: Mapping[str, Any]) -> ModelType:
        raise NotImplementedError()


class IUpdater(
    Generic[ModelType],
    IRepositoryMixin,
    metaclass=ABCMeta,
):
    async def update(self, model: ModelType) -> None:

        query = self._table. \
            update(). \
            values(self._make_update_mapping(model)). \
            where(self._make_where_for_update(model))

        async with self._connect() as conn:
            await conn.execute(query)

    @abstractmethod
    def _make_update_mapping(self, model: ModelType) -> Mapping[sa.Column, Any]:
        raise NotImplementedError()

    @abstractmethod
    def _make_where_for_update(self, model: ModelType) -> sa.sql.ColumnElement:
        raise NotImplementedError()


class IDeleter(
    IRepositoryMixin,
    metaclass=ABCMeta,
):
    async def delete(self, model_id: Id) -> None:
        query = self._table. \
            delete(). \
            where(self._make_where_for_delete(model_id))

        async with self._connect() as conn:
            await conn.execute(query)

    @abstractmethod
    def _make_where_for_delete(self, model_id: Id) -> sa.sql.ColumnElement:
        raise NotImplementedError()


class IRepository(
    ICreator[ModelType],
    IReader[ModelType, SpecificationType],
    IUpdater[ModelType],
    IDeleter,
    metaclass=ABCMeta,
):
    pass
