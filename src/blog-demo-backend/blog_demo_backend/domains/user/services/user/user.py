import datetime
from typing import Union
from uuid import uuid4

from blog_demo_backend.domains.user import User, UserSession
from blog_demo_backend.domains.shared import (
    IRepository,
    IPermissionService,
    ServiceError,
    InvalidRequest,
    NotFound,
    BaseService,
    IReader,
    ICreator,
    ByUserId,
)

from ...spec import UserById, UserByNickname
from ...shared import create_hash

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
            user_repository: IRepository[User, Union[UserById, UserByNickname]],
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

        user_with_nickname = await self._user_repository.read(UserByNickname(
            nickname=request.nickname,
        ))
        if user_with_nickname is not None:
            return InvalidRequest(
                description='user-already-exists',
            )

        model = User(
            id=uuid4().hex,
            nickname=request.nickname,
            role='user',
            created=datetime.datetime.now(),
            modified=datetime.datetime.now(),
        )
        await self._user_repository.create(model)
        await self._session_repository.create(UserSession(
            user_id=model.id,
            token=create_hash(
                nickname=model.nickname,
                password=request.password,
            ),
        ))

        return CreateUserResponse(model)

    async def _do_read(
            self,
            request: GetUserRequest,
    ) -> Union[GetUserResponse, ServiceError]:

        user = await self._user_repository.read(UserById(
            user_id=request.user_id,
        ))

        if isinstance(user, User):
            return GetUserResponse(user)
        else:
            return NotFound('user-not-found-by-id')

    async def _do_update(
            self,
            request: UpdateUserRequest,
    ) -> Union[UpdateUserResponse, ServiceError]:

        user = await self._user_repository.read(UserById(
            user_id=request.user_id,
        ))
        if isinstance(user, User):
            user.nickname = request.nickname
            user.modified = datetime.datetime.now()

            await self._user_repository.create(user)
            return UpdateUserResponse(user)
        else:
            return NotFound('user-not-found-by-id')

    async def _do_delete(
            self,
            request: DeleteUserRequest,
    ) -> Union[DeleteUserResponse, ServiceError]:

        user = await self._user_repository.read(UserById(
            user_id=request.user_id,
        ))
        if user is None:
            return NotFound('user-not-found-by-id')

        await self._user_repository.delete(request.user_id)
        return DeleteUserResponse()
