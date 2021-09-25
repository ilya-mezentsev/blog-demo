import datetime
from dataclasses import dataclass

from blog_demo_backend.domains.shared import Id


__all__ = [
    'User',
]


@dataclass
class User:
    id: Id
    nickname: str
    created: datetime.datetime
