from typing import Union, Any

from blog_demo_backend.domains.article import Comment
from blog_demo_backend.domains.shared import (
    IRepository,
    IPermissionService,
    ServiceError,
    BaseService,
)

from .request import *


__all__ = [
    'CommentService',
]


class CommentService(
    BaseService[
        CreateCommentRequest,
        CreateCommentResponse,
        GetCommentsRequest,
        GetCommentsResponse,
        UpdateCommentRequest,
        UpdateCommentResponse,
        DeleteCommentRequest,
        DeleteCommentResponse,
    ]
):
    """
    Сервис для управления комментариями к статьям. Чтение, удаление и т.д.
    """

    def __init__(
            self,
            # fixme Any -> some spec type
            repository: IRepository[Comment, Any],
            permission_service: IPermissionService,
    ) -> None:

        super().__init__(
            permission_service=permission_service,
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
