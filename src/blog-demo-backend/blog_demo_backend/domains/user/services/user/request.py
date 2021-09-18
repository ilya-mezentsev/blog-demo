from dataclasses import dataclass

from blog_demo_backend.domains.shared import Requester


__all__ = [
    'GetUserRequest', 'GetUserResponse',
    'CreateUserRequest', 'CreateUserResponse',
    'UpdateUserRequest', 'UpdateUserResponse',
    'DeleteUserRequest', 'DeleteUserResponse',
]


@dataclass
class GetUserRequest(Requester):
    ...


@dataclass
class GetUserResponse:
    ...


@dataclass
class CreateUserRequest(Requester):
    ...


@dataclass
class CreateUserResponse:
    ...


@dataclass
class UpdateUserRequest(Requester):
    ...


@dataclass
class UpdateUserResponse:
    ...


@dataclass
class DeleteUserRequest(Requester):
    ...


@dataclass
class DeleteUserResponse:
    ...
