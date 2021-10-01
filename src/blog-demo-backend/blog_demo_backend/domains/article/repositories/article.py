from typing import (
    Sequence,
    Optional,
)

from blog_demo_backend.shared import DBConnectionFn
from blog_demo_backend.domains.shared import IRepository, Id

from ..models import Article
from ..spec import ArticleById


__all__ = [
    'ArticleRepository',
]


class ArticleRepository(IRepository[Article, ArticleById]):
    def __init__(
            self,
            connection_fn: DBConnectionFn,
    ) -> None:

        self._connect = connection_fn

    async def create(self, model: Article) -> None:
        raise NotImplementedError()

    async def _read(self, specification: ArticleById) -> Optional[Article]:
        raise NotImplementedError()

    async def _read_all(self) -> Sequence[Article]:
        raise NotImplementedError()

    async def update(self, model: Article) -> None:
        raise NotImplementedError()

    async def delete(self, model_id: Id) -> None:
        raise NotImplementedError()
