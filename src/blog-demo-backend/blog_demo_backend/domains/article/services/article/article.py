from typing import Union

from blog_demo_backend.domains.article import Article
from blog_demo_backend.domains.shared import (
    IRepository,
    IPermissionService,
    ServiceError,
    BaseService,
    IReader,
    ByUserId,
)

from ...spec import ArticleById

from .request import *
from .settings import ArticleSettings


__all__ = [
    'ArticleService',
]


class ArticleService(
    BaseService[
        CreateArticleRequest,
        Union[GetArticlesRequest, GetArticleRequest],
        UpdateArticleRequest,
        DeleteArticleRequest,
    ]
):
    """
    Сервис для управления статьями. Чтение, удаление и т.д.
    """

    def __init__(
            self,
            settings: ArticleSettings,
            repository: IRepository[Article, ArticleById],
            permission_service: IPermissionService,
            user_role_repository: IReader[str, ByUserId],
    ) -> None:

        super().__init__(
            permission_service=permission_service,
            user_role_repository=user_role_repository,
        )

        self._settings = settings
        self._repository = repository

    async def _resource_id(
            self,
            request: Union[
                CreateArticleRequest,
                Union[GetArticlesRequest, GetArticleRequest],
                UpdateArticleRequest,
                DeleteArticleRequest,
            ],
    ) -> str:

        if isinstance(request, (UpdateArticleRequest, DeleteArticleRequest)):
            article = await self._repository.read(ArticleById(
                article_id=request.article_id,
            ))

            if (
                isinstance(article, Article) and
                article.author_id == request.request_user_id
            ):
                return 'own-article'

        return 'article'

    async def _do_create(
            self,
            request: CreateArticleRequest,
    ) -> Union[CreateArticleResponse, ServiceError]:

        raise NotImplementedError()

    async def _do_read(
            self,
            request: Union[GetArticlesRequest, GetArticleRequest],
    ) -> Union[Union[GetArticlesResponse, GetArticleResponse], ServiceError]:

        if isinstance(request, GetArticlesRequest):
            return await self._read_articles(request)

        elif isinstance(request, GetArticleRequest):
            return await self._read_article(request)

        else:
            raise RuntimeError(f'Unknown request type: {type(request)!r}')

    async def _read_articles(
            self,
            request: GetArticlesRequest,
    ) -> GetArticlesResponse:

        raise NotImplementedError()

    async def _read_article(
            self,
            request: GetArticleRequest,
    ) -> GetArticleResponse:

        raise NotImplementedError()

    async def _do_update(
            self,
            request: UpdateArticleRequest,
    ) -> Union[UpdateArticleResponse, ServiceError]:

        raise NotImplementedError()

    async def _do_delete(
            self,
            request: DeleteArticleRequest,
    ) -> Union[DeleteArticleResponse, ServiceError]:

        raise NotImplementedError()
