from typing import (
    Sequence,
    Optional,
    Union,
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

        self._connect = connection_fn

    async def create(self, model: User) -> None:

        query = user_table. \
            insert(). \
            values({
                user_table.c.uuid: model.id,
                user_table.c.role: model.role,
                user_table.c.nickname: model.nickname,
                user_table.c.created: model.created,
                user_table.c.modified: model.modified,
            })

        async with self._connect() as conn:
            await conn.execute(query)

    async def _read(self, specification: Union[UserById, UserByNickname]) -> Optional[User]:

        query = sa. \
            select([user_table]). \
            where(sa.and_(
                user_table.c.uuid == specification.user_id
                if isinstance(specification, UserById) else sa.or_(),

                user_table.c.nickname == specification.nickname
                if isinstance(specification, UserByNickname) else sa.or_(),
            ))

        async with self._connect() as conn:
            user_result = await conn.execute(query)
            user_row = user_result.fetchone()

        if user_row:
            return User(
                id=user_row['uuid'],
                role=user_row['role'],
                nickname=user_row['nickname'],
                created=user_row['created'],
                modified=user_row['modified'],
            )
        else:
            return None

    async def _read_all(self) -> Sequence[User]:
        raise NotImplementedError()

    async def update(self, model: User) -> None:

        query = user_table. \
            update(). \
            values({
                user_table.c.role: model.role,
                user_table.c.nickname: model.nickname,
                user_table.c.modified: model.modified,
            }). \
            where(user_table.c.uuid == model.id)

        async with self._connect() as conn:
            await conn.execute(query)

    async def delete(self, model_id: Id) -> None:

        query = user_table. \
            delete(). \
            where(user_table.c.uuid == model_id)

        async with self._connect() as conn:
            await conn.execute(query)
