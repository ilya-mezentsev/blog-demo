import datetime
from typing import Union
from uuid import uuid4

from blog_demo_backend.domains.article import Article
from blog_demo_backend.domains.shared import (
    IRepository,
    IPermissionService,
    ServiceError,
    NotFound,
    BaseService,
    IReader,
    ByUserId,
)

from ...spec import ArticleById

from .request import *


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
            article_repository: IRepository[Article, ArticleById],
            permission_service: IPermissionService,
            user_role_repository: IReader[str, ByUserId],
    ) -> None:

        super().__init__(
            permission_service=permission_service,
            user_role_repository=user_role_repository,
        )

        self._article_repository = article_repository

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
            article = await self._article_repository.read_one(ArticleById(
                article_id=request.article_id,
            ))

            if (
                article is not None and
                article.author_id == request.request_user_id
            ):
                return 'own-article'

        return 'article'

    async def _do_create(
            self,
            request: CreateArticleRequest,
    ) -> Union[CreateArticleResponse, ServiceError]:

        assert request.request_user_id

        article = Article(
            id=str(uuid4()),
            author_id=request.request_user_id,
            title=request.title,
            description=request.description,
            content=request.content,
            created=datetime.datetime.now(),
            modified=datetime.datetime.now(),
        )
        await self._article_repository.create(article)

        return CreateArticleResponse(article)

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
            _: GetArticlesRequest,
    ) -> GetArticlesResponse:

        return GetArticlesResponse(
            articles=(await self._article_repository.read_all()),
        )

    async def _read_article(
            self,
            request: GetArticleRequest,
    ) -> Union[GetArticleResponse, ServiceError]:

        article = await self._article_repository.read_one(ArticleById(
            article_id=request.article_id,
        ))
        if article is not None:
            return GetArticleResponse(article)
        else:
            return NotFound('article-not-found')

    async def _do_update(
            self,
            request: UpdateArticleRequest,
    ) -> Union[UpdateArticleResponse, ServiceError]:

        article = await self._article_repository.read_one(ArticleById(
            article_id=request.article_id,
        ))
        if article is None:
            return NotFound('article-not-found')

        article.title = request.title
        article.description = request.description
        article.modified = datetime.datetime.now()
        if request.content:
            article.content = request.content

        await self._article_repository.update(article)

        return UpdateArticleResponse(article)

    async def _do_delete(
            self,
            request: DeleteArticleRequest,
    ) -> Union[DeleteArticleResponse, ServiceError]:

        article = await self._article_repository.read_one(ArticleById(
            article_id=request.article_id,
        ))
        if article is None:
            return NotFound('article-not-found')

        await self._article_repository.delete(article.id)

        return DeleteArticleResponse()
