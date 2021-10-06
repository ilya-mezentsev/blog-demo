from dataclasses import dataclass

from blog_demo_backend.domains.user import UserSession, User
from blog_demo_backend.domains.shared import CreateResponse


__all__ = [
    'CreateSessionRequest', 'CreateSessionResponse',
]


@dataclass
class CreateSessionRequest:
    nickname: str
    password: str


@dataclass
class CreateSessionResponse(CreateResponse):
    session_key: str
