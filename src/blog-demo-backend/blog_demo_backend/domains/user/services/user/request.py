from dataclasses import dataclass
from typing import Iterable

from blog_demo_backend.domains.user import User
from blog_demo_backend.domains.shared import (
    Requester,
    Id,
    CreateResponse,
    ReadResponse,
    UpdateResponse,
    DeleteResponse,
)


__all__ = [
    'GetUserRequest', 'GetUserResponse',
    'GetUsersRequest', 'GetUsersResponse',
    'CreateUserRequest', 'CreateUserResponse',
    'UpdateUserRequest', 'UpdateUserResponse',
    'DeleteUserRequest', 'DeleteUserResponse',
]


@dataclass
class GetUserRequest(Requester):
    user_id: Id


@dataclass
class GetUserResponse(ReadResponse):
    user: User


@dataclass
class GetUsersRequest(Requester):
    pass


@dataclass
class GetUsersResponse(ReadResponse):
    users: Iterable[User]


@dataclass
class CreateUserRequest(Requester):
    nickname: str
    password: str


@dataclass
class CreateUserResponse(CreateResponse):
    user: User


@dataclass
class UpdateUserRequest(Requester):
    user_id: Id
    nickname: str


@dataclass
class UpdateUserResponse(UpdateResponse):
    user: User


@dataclass
class DeleteUserRequest(Requester):
    user_id: Id


@dataclass
class DeleteUserResponse(DeleteResponse):
    pass
