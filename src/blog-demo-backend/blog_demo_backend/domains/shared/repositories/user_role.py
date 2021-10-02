from typing import Sequence, Optional

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

    async def _read(self, specification: ByUserId) -> Optional[str]:

        query = sa. \
            select([user_table.c.role]). \
            where(user_table.c.uuid == specification.user_id)

        async with self._connection_fn() as conn:
            user_result = await conn.execute(query)
            user_row = user_result.fetchone()

        if user_row:
            return user_row['role']
        else:
            return None

    async def _read_all(self) -> Sequence[str]:
        raise NotImplementedError()
