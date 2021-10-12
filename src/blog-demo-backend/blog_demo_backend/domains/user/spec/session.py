from dataclasses import dataclass

from blog_demo_backend.domains.shared import Id


__all__ = [
    'SessionByUserIdAndToken',
]


@dataclass
class SessionByUserIdAndToken:
    user_id: Id
    token: str
