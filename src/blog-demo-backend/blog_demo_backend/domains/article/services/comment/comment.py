import datetime
import logging
from typing import Union
from uuid import uuid4

from blog_demo_backend.domains.article import Comment, Article
from blog_demo_backend.domains.shared import (
    IRepository,
    IPermissionService,
    ServiceError,
    NotFound,
    BaseService,
    IReader,
    ByUserId,
    IntegrityError,
)

from ...spec import (
    CommentByIds,
    CommentsByArticleId,
    ArticleById,
)

from .request import *


__all__ = [
    'CommentService',
]


class CommentService(
    BaseService[
        CreateCommentRequest,
        GetCommentsRequest,
        UpdateCommentRequest,
        DeleteCommentRequest,
    ]
):
    """
    Сервис для управления комментариями к статьям. Чтение, удаление и т.д.
    """

    def __init__(
            self,
            comment_repository: IRepository[
                Comment,
                Union[CommentByIds, CommentsByArticleId],
            ],
            article_repository: IReader[Article, ArticleById],
            permission_service: IPermissionService,
            user_role_repository: IReader[str, ByUserId],
    ) -> None:

        super().__init__(
            permission_service=permission_service,
            user_role_repository=user_role_repository,
        )

        self._comment_repository = comment_repository
        self._article_repository = article_repository

    async def _resource_id(
            self,
            request: Union[
                CreateCommentRequest,
                GetCommentsRequest,
                UpdateCommentRequest,
                DeleteCommentRequest,
            ],
    ) -> str:

        if isinstance(request, (UpdateCommentRequest, DeleteCommentRequest)):
            comment = await self._comment_repository.read_one(CommentByIds(
                article_id=request.article_id,
                comment_id=request.comment_id,
            ))

            if (
                comment is not None and
                comment.author_id == request.request_user_id
            ):
                return 'own-comment'

        return 'comment'

    async def _do_create(
            self,
            request: CreateCommentRequest,
    ) -> Union[CreateCommentResponse, ServiceError]:

        assert request.request_user_id is not None

        article = await self._article_repository.read_one(ArticleById(
            article_id=request.article_id,
        ))
        if article is None:
            return NotFound('article-not-found')

        comment = Comment(
            id=str(uuid4()),
            article_id=request.article_id,
            author_id=request.request_user_id,
            text=request.text,
            created=datetime.datetime.now(),
            modified=datetime.datetime.now(),
        )

        try:
            await self._comment_repository.create(comment)
            return CreateCommentResponse(comment)
        except IntegrityError:
            logging.error(
                f'Unable to create comment for article with id - {request.article_id}')
            return NotFound('article-not-found')

    async def _do_read(
            self,
            request: GetCommentsRequest,
    ) -> Union[GetCommentsResponse, ServiceError]:

        article = await self._article_repository.read_one(ArticleById(
            article_id=request.article_id,
        ))
        if not isinstance(article, Article):
            return NotFound('article-not-found')

        comments = await self._comment_repository.read_all(CommentsByArticleId(
            article_id=request.article_id,
        ))

        return GetCommentsResponse(comments)

    async def _do_update(
            self,
            request: UpdateCommentRequest,
    ) -> Union[UpdateCommentResponse, ServiceError]:

        comment = await self._comment_repository.read_one(CommentByIds(
            article_id=request.article_id,
            comment_id=request.comment_id,
        ))
        if comment is None:
            return NotFound('comment-not-found')

        comment.text = request.text
        await self._comment_repository.update(comment)

        return UpdateCommentResponse(comment)

    async def _do_delete(
            self,
            request: DeleteCommentRequest,
    ) -> Union[DeleteCommentResponse, ServiceError]:

        comment = await self._comment_repository.read_one(CommentByIds(
            article_id=request.article_id,
            comment_id=request.comment_id,
        ))
        if comment is None:
            return NotFound('comment-not-found')

        await self._comment_repository.delete(request.comment_id)

        return DeleteCommentResponse()
