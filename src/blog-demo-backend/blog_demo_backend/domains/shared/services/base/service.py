from abc import ABCMeta, abstractmethod
from typing import (
    TypeVar,
    Generic,
    Union,
)

from blog_demo_backend.domains.shared import (
    Requester,
    IPermissionService,
    PermissionRequest,
    Operation,
    ServiceError,
    ForbiddenError,
)


__all__ = [
    'BaseService',
]


CreateRequest = TypeVar('CreateRequest', bound=Requester)
CreateResponse = TypeVar('CreateResponse')
ReadRequest = TypeVar('ReadRequest', bound=Requester)
ReadResponse = TypeVar('ReadResponse')
UpdateRequest = TypeVar('UpdateRequest', bound=Requester)
UpdateResponse = TypeVar('UpdateResponse')
DeleteRequest = TypeVar('DeleteRequest', bound=Requester)
DeleteResponse = TypeVar('DeleteResponse')


class BaseService(
    Generic[
        CreateRequest,
        CreateResponse,
        ReadRequest,
        ReadResponse,
        UpdateRequest,
        UpdateResponse,
        DeleteRequest,
        DeleteResponse,
    ],
    metaclass=ABCMeta,
):
    """
    Базовый сервис для CRUD сервисов.
    Пока в его задачи входит только прочерить доступ клиента до ресурса
    """

    def __init__(
            self,
            permission_service: IPermissionService,
    ) -> None:

        self._permission_service = permission_service

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

        if not (await self._permission_service.has_permission(PermissionRequest(
            role_id=request.role_id,
            resource_id=(await self._resource_id(request)),
            operation=Operation.CREATE,
        ))):
            return ForbiddenError()

        return await self._do_create(request)

    @abstractmethod
    async def _do_create(self, request: CreateRequest) -> Union[CreateResponse, ServiceError]:
        raise NotImplementedError()

    async def read(self, request: ReadRequest) -> Union[ReadResponse, ServiceError]:

        if not (await self._permission_service.has_permission(PermissionRequest(
            role_id=request.role_id,
            resource_id=(await self._resource_id(request)),
            operation=Operation.READ,
        ))):
            return ForbiddenError()

        return await self._do_read(request)

    @abstractmethod
    async def _do_read(self, request: ReadRequest) -> Union[ReadResponse, ServiceError]:
        raise NotImplementedError()

    async def update(self, request: UpdateRequest) -> Union[UpdateResponse, ServiceError]:

        if not (await self._permission_service.has_permission(PermissionRequest(
            role_id=request.role_id,
            resource_id=(await self._resource_id(request)),
            operation=Operation.UPDATE,
        ))):
            return ForbiddenError()

        return await self._do_update(request)

    @abstractmethod
    async def _do_update(self, request: UpdateRequest) -> Union[UpdateResponse, ServiceError]:
        raise NotImplementedError()

    async def delete(self, request: DeleteRequest) -> Union[DeleteResponse, ServiceError]:

        if not (await self._permission_service.has_permission(PermissionRequest(
            role_id=request.role_id,
            resource_id=(await self._resource_id(request)),
            operation=Operation.DELETE,
        ))):
            return ForbiddenError()

        return await self._do_delete(request)

    @abstractmethod
    async def _do_delete(self, request: DeleteRequest) -> Union[DeleteResponse, ServiceError]:
        raise NotImplementedError()
