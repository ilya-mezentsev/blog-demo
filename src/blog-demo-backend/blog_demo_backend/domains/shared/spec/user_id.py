from dataclasses import dataclass

from .base import BaseSpec
from ..types import Id


__all__ = [
    'ByUserId',
]


@dataclass
class ByUserId(BaseSpec):
    user_id: Id
