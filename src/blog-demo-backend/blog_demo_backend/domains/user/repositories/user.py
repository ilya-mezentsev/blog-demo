from typing import (
    Union,
    Mapping,
    Any,
)

import sqlalchemy as sa  # type: ignore

from blog_demo_backend.db import get_table
from blog_demo_backend.shared import DBConnectionFn
from blog_demo_backend.domains.shared import IRepository, Id
from blog_demo_backend.domains.user import User

from ..spec import UserById, UserByNickname


__all__ = [
    'UserRepository',
]


user_table = get_table('user')


class UserRepository(
    IRepository[
        User,
        Union[UserById, UserByNickname],
    ]
):
    def __init__(
            self,
            connection_fn: DBConnectionFn,
    ) -> None:

        self._connection_fn = connection_fn

    def _make_create_mapping(self, model: User) -> Mapping[sa.Column, Any]:
        return {
            user_table.c.uuid: model.id,
            user_table.c.role: model.role,
            user_table.c.nickname: model.nickname,
            user_table.c.created: model.created,
            user_table.c.modified: model.modified,
        }

    def _make_where_for_read(self, specification: Union[UserById, UserByNickname]) -> sa.sql.ColumnElement:
        if isinstance(specification, UserById):
            return user_table.c.uuid == specification.user_id

        elif isinstance(specification, UserByNickname):
            return user_table.c.nickname == specification.nickname

        else:
            raise RuntimeError(
                f'Unknown specification type: {type(specification)!r}')

    def _model_from_row(self, user_row: Mapping[str, Any]) -> User:
        return User(
            id=user_row['uuid'],
            role=user_row['role'],
            nickname=user_row['nickname'],
            created=user_row['created'],
            modified=user_row['modified'],
        )

    def _make_update_mapping(self, model: User) -> Mapping[sa.Column, Any]:
        return {
            user_table.c.role: model.role,
            user_table.c.nickname: model.nickname,
            user_table.c.modified: model.modified,
        }

    def _make_where_for_update(self, model: User) -> sa.sql.ColumnElement:
        return user_table.c.uuid == model.id

    def _make_where_for_delete(self, model_id: Id) -> sa.sql.ColumnElement:
        return user_table.c.uuid == model_id

    @property
    def _table(self) -> sa.Table:
        return user_table

    @property
    def _connect(self) -> DBConnectionFn:
        return self._connection_fn
