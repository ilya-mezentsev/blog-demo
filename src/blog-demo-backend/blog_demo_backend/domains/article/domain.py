from blog_demo_backend.shared import DBConnectionFn
from blog_demo_backend.domains.shared import (
    IPermissionService,
    IReader,
    ByUserId,
    CacheFactoryFn,
)
from blog_demo_backend.domains.article import (
    ArticleRepository,
    ArticleService,
    CommentService,
    CommentRepository,
)


__all__ = [
    'ArticleDomain',
]


class ArticleDomain:

    class EntityTypes:
        ARTICLE = 'article'
        COMMENT = 'comment'

    def __init__(
            self,
            cache_factory_fn: CacheFactoryFn,
            connection_fn: DBConnectionFn,
            permission_service: IPermissionService,
            user_role_repository: IReader[str, ByUserId],
    ) -> None:

        self.article_cache = cache_factory_fn(self.EntityTypes.ARTICLE)
        self.comment_cache = cache_factory_fn(self.EntityTypes.COMMENT)

        article_repository = ArticleRepository(
            connection_fn=connection_fn,
            cache=self.article_cache,
        )

        self.article_service = ArticleService(
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

    async def on_cache_changed(self, entity_type: str) -> None:
        if entity_type == self.EntityTypes.ARTICLE:
            await self.article_cache.reset_cache()

        elif entity_type == self.EntityTypes.COMMENT:
            await self.comment_cache.reset_cache()
