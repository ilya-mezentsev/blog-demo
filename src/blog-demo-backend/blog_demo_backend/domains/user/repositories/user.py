from typing import (
    Sequence,
    Any,
    Optional,
)

from blog_demo_backend.shared import DBConnectionFn
from blog_demo_backend.domains.shared import IRepository, Id
from blog_demo_backend.domains.user import User


__all__ = [
    'UserRepository',
]


# fixme Any -> some spec type
class UserRepository(IRepository[User, Any]):
    def __init__(
            self,
            connection_fn: DBConnectionFn,
    ) -> None:

        self._connect = connection_fn

    async def create(self, model: User) -> None:
        raise NotImplementedError()

    async def _read(self, specification: Any) -> Optional[User]:
        raise NotImplementedError()

    async def _read_all(self) -> Sequence[User]:
        raise NotImplementedError()

    async def update(self, model: User) -> None:
        raise NotImplementedError()

    async def delete(self, model_id: Id) -> None:
        raise NotImplementedError()
