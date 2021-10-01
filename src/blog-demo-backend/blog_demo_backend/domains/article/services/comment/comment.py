from typing import Union

from blog_demo_backend.domains.article import Comment
from blog_demo_backend.domains.shared import (
    IRepository,
    IPermissionService,
    ServiceError,
    BaseService,
    IReader,
    ByUserId,
)

from ...spec import (
    CommentByIds,
    CommentsByArticleId,
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
            repository: IRepository[
                Comment,
                Union[CommentByIds, CommentsByArticleId],
            ],
            permission_service: IPermissionService,
            user_role_repository: IReader[str, ByUserId],
    ) -> None:

        super().__init__(
            permission_service=permission_service,
            user_role_repository=user_role_repository,
        )

        self._repository = repository

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
            comment = await self._repository.read(CommentByIds(
                article_id=request.article_id,
                comment_id=request.comment_id,
            ))

            if (
                isinstance(comment, Comment) and
                comment.author_id == request.request_user_id
            ):
                return 'own-comment'

        return 'comment'

    async def _do_create(
            self,
            request: CreateCommentRequest,
    ) -> Union[CreateCommentResponse, ServiceError]:

        raise NotImplementedError()

    async def _do_read(
            self,
            request: GetCommentsRequest,
    ) -> Union[GetCommentsResponse, ServiceError]:

        raise NotImplementedError()

    async def _do_update(
            self,
            request: UpdateCommentRequest,
    ) -> Union[UpdateCommentResponse, ServiceError]:

        raise NotImplementedError()

    async def _do_delete(
            self,
            request: DeleteCommentRequest,
    ) -> Union[DeleteCommentResponse, ServiceError]:

        raise NotImplementedError()
