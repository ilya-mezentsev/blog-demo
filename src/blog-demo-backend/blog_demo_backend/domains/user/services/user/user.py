from typing import Union

from blog_demo_backend.domains.user import User, UserSession
from blog_demo_backend.domains.shared import (
    IRepository,
    IPermissionService,
    ServiceError,
    BaseService,
    IReader,
    ICreator,
    ByUserId,
)

from ...spec import UserById

from .request import *


__all__ = [
    'UserService',
]


class UserService(
    BaseService[
        CreateUserRequest,
        GetUserRequest,
        UpdateUserRequest,
        DeleteUserRequest,
    ]
):
    """
    Сервис для управления пользователями.
    """

    def __init__(
            self,
            user_repository: IRepository[User, UserById],
            session_repository: ICreator[UserSession],
            permission_service: IPermissionService,
            user_role_repository: IReader[str, ByUserId],
    ) -> None:

        super().__init__(
            permission_service=permission_service,
            user_role_repository=user_role_repository,
        )

        self._user_repository = user_repository
        self._session_repository = session_repository

    async def _resource_id(self, request: Union[
        CreateUserRequest,
        GetUserRequest,
        UpdateUserRequest,
        DeleteUserRequest,
    ]) -> str:

        if isinstance(
            request,
            (
                GetUserRequest,
                UpdateUserRequest,
                DeleteUserRequest,
            ),
        ):
            if request.user_id == request.request_user_id:
                return 'self-user'

        return 'user'

    async def _do_create(
            self,
            request: CreateUserRequest,
    ) -> Union[CreateUserResponse, ServiceError]:

        raise NotImplementedError()

    async def _do_read(
            self,
            request: GetUserRequest,
    ) -> Union[GetUserResponse, ServiceError]:

        raise NotImplementedError()

    async def _do_update(
            self,
            request: UpdateUserRequest,
    ) -> Union[UpdateUserResponse, ServiceError]:

        raise NotImplementedError()

    async def _do_delete(
            self,
            request: DeleteUserRequest,
    ) -> Union[DeleteUserResponse, ServiceError]:

        raise NotImplementedError()
