from dataclasses import dataclass

from .id import Id


__all__ = [
    'Requester',
]


@dataclass
class Requester:
    request_user_id: Id
