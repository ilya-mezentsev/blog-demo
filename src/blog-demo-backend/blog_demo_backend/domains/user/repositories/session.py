from typing import (
    Sequence,
    Optional,
)

import sqlalchemy as sa  # type: ignore

from blog_demo_backend.db import get_table
from blog_demo_backend.shared import DBConnectionFn
from blog_demo_backend.domains.user import UserSession

from ..spec import SessionByHash
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

        self._connect = connection_fn

    async def create(self, model: UserSession) -> None:
        query = user_token_table.insert().values({
            'user_id': model.user_id,
            'token': model.token,
        })

        async with self._connect() as conn:
            await conn.execute(query)

    async def _read(self, specification: SessionByHash) -> Optional[UserSession]:

        query = sa. \
            select([user_token_table]). \
            where(user_token_table.c.token == specification.hash)

        async with self._connect() as conn:
            session_result = await conn.execute(query)
            session_row = session_result.fetchone()

        if session_row:
            return UserSession(
                user_id=session_row['user_id'],
                token=session_row['token'],
            )
        else:
            return None

    async def _read_all(self) -> Sequence[UserSession]:
        raise NotImplementedError()
