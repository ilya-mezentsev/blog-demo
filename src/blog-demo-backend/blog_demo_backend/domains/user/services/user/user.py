import datetime
from typing import Union
from uuid import uuid4

from blog_demo_backend.domains.user import (
    User,
    UserSession,
)
from blog_demo_backend.domains.shared import (
    ICreator,
    IPermissionService,
    ServiceError,
    InvalidRequest,
    NotFound,
    BaseService,
    IReader,
    ByUserId,
)

from ...shared import create_hash
from ...spec import UserById, UserByNickname
from ...types import IUserRepository

from .request import *


__all__ = [
    'UserService',
]


class UserService(
    BaseService[
        CreateUserRequest,
        Union[GetUserRequest, GetUsersRequest],
        UpdateUserRequest,
        DeleteUserRequest,
    ]
):
    """
    Сервис для управления пользователями.
    """

    def __init__(
            self,
            user_repository: IUserRepository,
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
        Union[GetUserRequest, GetUsersRequest],
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
                return 'self'

        return 'user'

    async def _do_create(
            self,
            request: CreateUserRequest,
    ) -> Union[CreateUserResponse, ServiceError]:

        user_with_nickname = await self._user_repository.read_one(UserByNickname(
            nickname=request.nickname,
        ))
        if user_with_nickname is not None:
            return InvalidRequest(
                description='nickname-already-exists',
            )

        model = User(
            id=str(uuid4()),
            nickname=request.nickname,
            role='user',
            created=datetime.datetime.now(),
            modified=datetime.datetime.now(),
        )
        await self._user_repository.create(model)
        await self._session_repository.create(UserSession(
            user_id=model.id,
            token=create_hash(request.password),
        ))

        return CreateUserResponse(model)

    async def _do_read(
            self,
            request: Union[GetUserRequest, GetUsersRequest],
    ) -> Union[Union[GetUserResponse, GetUsersResponse], ServiceError]:

        if isinstance(request, GetUserRequest):
            return await self._get_user(request)

        elif isinstance(request, GetUsersRequest):
            return await self._get_users(request)

        else:
            raise RuntimeError(f'Unknown request type: {type(request)!r}')

    async def _get_user(
            self,
            request: GetUserRequest,
    ) -> Union[GetUserResponse, ServiceError]:

        user = await self._user_repository.read_one(UserById(
            user_id=request.user_id,
        ))

        if user is not None:
            return GetUserResponse(user)
        else:
            return NotFound('user-not-found')

    async def _get_users(
            self,
            _: GetUsersRequest,
    ) -> GetUsersResponse:

        return GetUsersResponse(
            users=(await self._user_repository.read_all()),
        )

    async def _do_update(
            self,
            request: UpdateUserRequest,
    ) -> Union[UpdateUserResponse, ServiceError]:

        user = await self._user_repository.read_one(UserById(
            user_id=request.user_id,
        ))
        if user is None:
            return NotFound('user-not-found')

        user_with_nickname = await self._user_repository.read_one(UserByNickname(
            nickname=request.nickname,
        ))
        if user_with_nickname is not None:
            return InvalidRequest(
                description='nickname-already-exists',
            )

        user.nickname = request.nickname
        user.modified = datetime.datetime.now()

        await self._user_repository.update(user)
        return UpdateUserResponse(user)

    async def _do_delete(
            self,
            request: DeleteUserRequest,
    ) -> Union[DeleteUserResponse, ServiceError]:

        user = await self._user_repository.read_one(UserById(
            user_id=request.user_id,
        ))
        if user is None:
            return NotFound('user-not-found')

        await self._user_repository.delete(request.user_id)
        return DeleteUserResponse()
