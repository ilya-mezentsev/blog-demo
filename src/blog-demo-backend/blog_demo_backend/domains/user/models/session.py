from dataclasses import dataclass

from blog_demo_backend.domains.shared import Id


__all__ = [
    'UserSession',
]


@dataclass
class UserSession:
    user_id: Id
    token: str
