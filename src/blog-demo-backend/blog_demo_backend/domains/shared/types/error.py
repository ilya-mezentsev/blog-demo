from dataclasses import dataclass
from typing import Optional


__all__ = [
    'ServiceError',
    'ForbiddenError',
    'InvalidRequest',
    'NotFound',
]


@dataclass
class ServiceError:
    description: Optional[str] = None


@dataclass
class ForbiddenError(ServiceError):
    pass


@dataclass
class InvalidRequest(ServiceError):
    pass


@dataclass
class NotFound(ServiceError):
    pass
