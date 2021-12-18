from abc import ABCMeta, abstractmethod
from typing import (
    TypeVar,
    Generic,
    Union, Optional,
)

from ..permission import (
    IPermissionService,
    PermissionRequest,
    Operation,
)
from ...repositories import IReader
from ...spec import ByUserId
from ...types import (
    Requester,
    Id,
    ServiceError,
    ForbiddenError,
    CreateResponse,
    ReadResponse,
    UpdateResponse,
    DeleteResponse,
)


__all__ = [
    'BaseService',
]


CreateRequest = TypeVar('CreateRequest', bound=Requester)
ReadRequest = TypeVar('ReadRequest', bound=Requester)
UpdateRequest = TypeVar('UpdateRequest', bound=Requester)
DeleteRequest = TypeVar('DeleteRequest', bound=Requester)


class BaseService(
    Generic[
        CreateRequest,
        ReadRequest,
        UpdateRequest,
        DeleteRequest,
    ],
    metaclass=ABCMeta,
):
    """
    Базовый сервис для CRUD сервисов.
    Пока в его задачи входит только проверить доступ клиента до ресурса
    """

    _GUEST_ROLE = 'anonymous'

    def __init__(
            self,
            user_role_repository: IReader[str, ByUserId],
            permission_service: IPermissionService,
    ) -> None:

        self._permission_service = permission_service

        self._user_role_repository = user_role_repository

    @abstractmethod
    async def _resource_id(
            self,
            request: Union[
                CreateRequest,
                ReadRequest,
                UpdateRequest,
                DeleteRequest,
            ],
    ) -> str:
        """
        Данный метод предназначен для вычисления ID ресурса.
        Этот ID может поменяться в зав-ти от контекста (данных из запроса).
        Например, любой пользователь не может обновить статью; но автор статьи может
        """

        raise NotImplementedError()

    async def create(self, request: CreateRequest) -> Union[CreateResponse, ServiceError]:

        if not (await self._permission_service.has_permission(await self._make_permission_request(
            request=request,
            operation=Operation.CREATE,
        ))):
            return ForbiddenError('operation-not-permitted')

        return await self._do_create(request)

    @abstractmethod
    async def _do_create(self, request: CreateRequest) -> Union[CreateResponse, ServiceError]:
        raise NotImplementedError()

    async def read(self, request: ReadRequest) -> Union[ReadResponse, ServiceError]:

        if not (await self._permission_service.has_permission(await self._make_permission_request(
            request=request,
            operation=Operation.READ,
        ))):
            return ForbiddenError('operation-not-permitted')

        return await self._do_read(request)

    @abstractmethod
    async def _do_read(self, request: ReadRequest) -> Union[ReadResponse, ServiceError]:
        raise NotImplementedError()

    async def update(self, request: UpdateRequest) -> Union[UpdateResponse, ServiceError]:

        if not (await self._permission_service.has_permission(await self._make_permission_request(
            request=request,
            operation=Operation.UPDATE,
        ))):
            return ForbiddenError('operation-not-permitted')

        return await self._do_update(request)

    @abstractmethod
    async def _do_update(self, request: UpdateRequest) -> Union[UpdateResponse, ServiceError]:
        raise NotImplementedError()

    async def delete(self, request: DeleteRequest) -> Union[DeleteResponse, ServiceError]:

        if not (await self._permission_service.has_permission(await self._make_permission_request(
            request=request,
            operation=Operation.DELETE,
        ))):
            return ForbiddenError('operation-not-permitted')

        return await self._do_delete(request)

    @abstractmethod
    async def _do_delete(self, request: DeleteRequest) -> Union[DeleteResponse, ServiceError]:
        raise NotImplementedError()

    async def _make_permission_request(
            self,
            request: Union[
                CreateRequest,
                ReadRequest,
                UpdateRequest,
                DeleteRequest,
            ],
            operation: Operation,
    ) -> PermissionRequest:

        return PermissionRequest(
            role_id=(await self._get_user_role(request.request_user_id)),
            resource_id=(await self._resource_id(request)),
            operation=operation,
            version_id=(await self._permission_service.get_roles_version()),
        )

    async def _get_user_role(self, user_id: Optional[Id]) -> str:
        if user_id is None:
            return self._GUEST_ROLE

        role_id = await self._user_role_repository.read_one(ByUserId(
            user_id=user_id,
        ))

        if isinstance(role_id, str):
            return role_id
        else:
            return self._GUEST_ROLE
