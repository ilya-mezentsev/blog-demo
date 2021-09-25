from typing import Union, Any

from blog_demo_backend.domains.user import User
from blog_demo_backend.domains.shared import (
    IRepository,
    IPermissionService,
    ServiceError,
    BaseService,
)

from .request import *


__all__ = [
    'UserService',
]


class UserService(
    BaseService[
        CreateUserRequest,
        CreateUserResponse,
        GetUserRequest,
        GetUserResponse,
        UpdateUserRequest,
        UpdateUserResponse,
        DeleteUserRequest,
        DeleteUserResponse,
    ]
):
    """
    Сервис для управления пользователями.
    """

    def __init__(
            self,
            repository: IRepository[User, Any],  # fixme Any -> some spec type
            permission_service: IPermissionService,
    ) -> None:

        super().__init__(
            permission_service=permission_service,
        )

        self._repository = repository

    async def _resource_id(self, request: Union[
        CreateUserRequest,
        GetUserRequest,
        UpdateUserRequest,
        DeleteUserRequest,
    ]) -> str:

        raise NotImplementedError()

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
