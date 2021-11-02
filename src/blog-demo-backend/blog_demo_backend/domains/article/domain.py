from blog_demo_backend.shared import DBConnectionFn
from blog_demo_backend.domains.shared import (
    IPermissionService,
    IReader,
    ByUserId,
    MemoryCache,
)
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
            article_settings: ArticleSettings,
            connection_fn: DBConnectionFn,
            permission_service: IPermissionService,
            user_role_repository: IReader[str, ByUserId],
    ) -> None:

        self.article_cache = MemoryCache()
        self.comment_cache = MemoryCache()

        article_repository = ArticleRepository(
            connection_fn=connection_fn,
            cache=self.article_cache,
        )

        self.article_service = ArticleService(
            settings=article_settings,
            article_repository=article_repository,
            permission_service=permission_service,
            user_role_repository=user_role_repository,
        )

        self.comment_service = CommentService(
            comment_repository=CommentRepository(
                connection_fn=connection_fn,
                cache=self.comment_cache,
            ),
            article_repository=article_repository,
            permission_service=permission_service,
            user_role_repository=user_role_repository,
        )
