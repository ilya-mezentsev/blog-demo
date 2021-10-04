from dataclasses import dataclass
from typing import Optional

from .id import Id


__all__ = [
    'Requester',
]


@dataclass
class Requester:
    request_user_id: Optional[Id]
