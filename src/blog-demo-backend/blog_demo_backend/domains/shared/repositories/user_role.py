from typing import Mapping, Any

import sqlalchemy as sa  # type: ignore

from blog_demo_backend.db import get_table
from blog_demo_backend.shared import DBConnectionFn
from ..spec import ByUserId

from .base import IReader


__all__ = [
    'UserRoleRepository',
]


user_table = get_table('user')


class UserRoleRepository(IReader[str, ByUserId]):

    def __init__(
            self,
            connection_fn: DBConnectionFn,
    ) -> None:

        self._connection_fn = connection_fn

    def _make_where_for_read(self, specification: ByUserId) -> sa.sql.ColumnElement:
        return user_table.c.uuid == specification.user_id

    def _model_from_row(self, user_row: Mapping[str, Any]) -> str:
        return user_row['role']

    @property
    def _table(self) -> sa.Table:
        return user_table

    @property
    def _connect(self) -> DBConnectionFn:
        return self._connection_fn
