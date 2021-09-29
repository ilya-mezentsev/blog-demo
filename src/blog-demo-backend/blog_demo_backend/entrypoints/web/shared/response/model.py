from dataclasses import dataclass
from typing import (
    Optional,
    Mapping,
    Any,
)


__all__ = [
    'ResponseModel',
]


@dataclass
class ResponseModel:
    http_status: int
    body: Optional[Mapping[str, Any]] = None
    headers: Optional[Mapping[str, str]] = None
