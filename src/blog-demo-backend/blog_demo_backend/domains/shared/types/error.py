from dataclasses import dataclass
from typing import Optional


__all__ = [
    'ServiceError',
    'ForbiddenError',
    'InvalidRequest',
]


@dataclass
class ServiceError:
    pass


@dataclass
class ForbiddenError(ServiceError):
    description: Optional[str] = None


@dataclass
class InvalidRequest(ServiceError):
    description: Optional[str] = None
