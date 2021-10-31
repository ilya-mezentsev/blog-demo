from dataclasses import dataclass

from blog_demo_backend.domains.shared import Id, BaseSpec


__all__ = [
    'UserById',
    'UserByNickname',
]


@dataclass
class UserById(BaseSpec):
    user_id: Id


@dataclass
class UserByNickname(BaseSpec):
    nickname: str
