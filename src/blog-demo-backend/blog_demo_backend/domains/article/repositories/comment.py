from typing import Sequence, Any

from blog_demo_backend.shared import DBConnectionFn
from blog_demo_backend.domains.shared import IRepository, Id
from blog_demo_backend.domains.article import Comment


__all__ = [
    'CommentRepository',
]


# fixme Any -> some spec type
class CommentRepository(IRepository[Comment, Any]):
    def __init__(
            self,
            connection_fn: DBConnectionFn,
    ) -> None:

        self._connect = connection_fn

    async def create(self, model: Comment) -> None:
        raise NotImplementedError()

    async def _read(self, specification: Any) -> Sequence[Comment]:
        raise NotImplementedError()

    async def _read_all(self) -> Sequence[Comment]:
        raise NotImplementedError()

    async def update(self, model: Comment) -> None:
        raise NotImplementedError()

    async def delete(self, model_id: Id) -> None:
        raise NotImplementedError()
