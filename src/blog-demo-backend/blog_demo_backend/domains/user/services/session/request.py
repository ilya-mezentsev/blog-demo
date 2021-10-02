from dataclasses import dataclass

from blog_demo_backend.domains.user import UserSession, User
from blog_demo_backend.domains.shared import CreateResponse


__all__ = [
    'CreateUserRequest', 'CreateUserResponse',
    'CreateSessionRequest', 'CreateSessionResponse',
]


@dataclass
class CreateUserRequest:
    nickname: str
    password: str


@dataclass
class CreateUserResponse(CreateResponse):
    user: User


@dataclass
class CreateSessionRequest:
    nickname: str
    password: str


@dataclass
class CreateSessionResponse(CreateResponse):
    session: UserSession
