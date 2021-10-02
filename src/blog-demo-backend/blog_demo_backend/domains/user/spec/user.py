from dataclasses import dataclass

from blog_demo_backend.domains.shared import Id


__all__ = [
    'UserById',
    'UserByNickname',
]


@dataclass
class UserById:
    user_id: Id


@dataclass
class UserByNickname:
    nickname: str
