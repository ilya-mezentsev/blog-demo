from dataclasses import dataclass

from ..types import Id


__all__ = [
    'ByUserId',
]


@dataclass
class ByUserId:
    user_id: Id
