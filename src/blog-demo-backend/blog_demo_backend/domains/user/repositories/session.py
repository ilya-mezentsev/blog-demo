from typing import (
    Mapping,
    Any,
)

import sqlalchemy as sa  # type: ignore

from blog_demo_backend.db import get_table
from blog_demo_backend.shared import DBConnectionFn
from blog_demo_backend.domains.user import UserSession

from ..spec import SessionByUserIdAndToken
from ..types import IUserSessionRepository


__all__ = [
    'UserSessionRepository',
]


user_token_table = get_table('user_token')


class UserSessionRepository(IUserSessionRepository):
    def __init__(
            self,
            connection_fn: DBConnectionFn,
    ) -> None:

        self._connection_fn = connection_fn

    def _make_create_mapping(self, model: UserSession) -> Mapping[sa.Column, Any]:
        return {
            user_token_table.c.user_id: model.user_id,
            user_token_table.c.token: model.token,
        }

    def _make_where_for_read(self, specification: SessionByUserIdAndToken) -> sa.sql.ColumnElement:
        return sa.and_(
            user_token_table.c.user_id == specification.user_id,
            user_token_table.c.token == specification.token,
        )

    def _model_from_row(self, session_row: Mapping[str, Any]) -> UserSession:
        return UserSession(
            user_id=session_row['user_id'],
            token=session_row['token'],
        )

    @property
    def _table(self) -> sa.Table:
        return user_token_table

    @property
    def _connect(self) -> DBConnectionFn:
        return self._connection_fn
