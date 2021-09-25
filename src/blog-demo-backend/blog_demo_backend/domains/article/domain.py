from blog_demo_backend.shared import DBConnectionFn
from blog_demo_backend.domains.shared import IPermissionService
from blog_demo_backend.domains.article import (
    ArticleSettings,
    ArticleRepository,
    ArticleService,
    CommentService,
    CommentRepository,
)


__all__ = [
    'ArticleDomain',
]


class ArticleDomain:

    def __init__(
            self,
            settings: ArticleSettings,
            connection_fn: DBConnectionFn,
            permission_service: IPermissionService,
    ) -> None:

        self.article_service = ArticleService(
            settings=settings,
            repository=ArticleRepository(
                connection_fn=connection_fn,
            ),
            permission_service=permission_service,
        )

        self.comment_service = CommentService(
            repository=CommentRepository(
                connection_fn=connection_fn,
            ),
            permission_service=permission_service,
        )
