from dataclasses import dataclass

from blog_demo_backend.domains.shared import Id, BaseSpec


__all__ = [
    'SessionByUserIdAndToken',
]


@dataclass
class SessionByUserIdAndToken(BaseSpec):
    user_id: Id
    token: str
