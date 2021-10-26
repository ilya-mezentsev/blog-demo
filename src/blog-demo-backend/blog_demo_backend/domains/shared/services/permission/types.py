from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Optional


__all__ = [
    'IPermissionService',
    'Operation',
    'PermissionRequest',
    'PermissionEffect',
]


class IPermissionService(metaclass=ABCMeta):

    @abstractmethod
    async def has_permission(
            self,
            request: 'PermissionRequest',
    ) -> bool:

        raise NotImplementedError()

    @abstractmethod
    async def get_roles_version(self) -> str:
        raise NotImplementedError()


class PermissionEffect(Enum):
    PERMIT = 'permit'
    DENY = 'deny'


class Operation(Enum):
    CREATE = 'create'
    READ = 'read'
    UPDATE = 'update'
    DELETE = 'delete'


@dataclass
class PermissionRequest:
    role_id: str
    resource_id: str
    operation: Operation
    version_id: Optional[str] = None

    def __str__(self) -> str:
        return f'{self.role_id}:{self.resource_id}:{self.operation.value}:{self.version_id}'
