from typing import (
    Sequence,
    Optional,
    Union,
)

from blog_demo_backend.shared import DBConnectionFn
from blog_demo_backend.domains.shared import IRepository, Id

from ..models import Comment
from ..spec import (
    CommentByIds,
    CommentsByArticleId,
)


__all__ = [
    'CommentRepository',
]


class CommentRepository(
    IRepository[
        Comment,
        Union[CommentByIds, CommentsByArticleId],
    ]
):
    def __init__(
            self,
            connection_fn: DBConnectionFn,
    ) -> None:

        self._connect = connection_fn

    async def create(self, model: Comment) -> None:
        raise NotImplementedError()

    async def _read(self, specification: Union[CommentByIds, CommentsByArticleId]) -> Optional[Comment]:
        raise NotImplementedError()

    async def _read_all(self) -> Sequence[Comment]:
        raise NotImplementedError()

    async def update(self, model: Comment) -> None:
        raise NotImplementedError()

    async def delete(self, model_id: Id) -> None:
        raise NotImplementedError()
