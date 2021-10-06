from abc import ABCMeta
from typing import Union

from blog_demo_backend.domains.shared import (
    ICreator,
    IReader,
    IUpdater,
    IDeleter,
)
from blog_demo_backend.domains.user import UserSession, User

from ..spec import (
    SessionByUserIdAndToken,
    UserById,
    UserByNickname,
)


__all__ = [
    'IUserSessionRepository',
    'IUserReaderRepository',
    'IUserRepository',
]


class IUserSessionRepository(
    ICreator[UserSession],
    IReader[UserSession, SessionByUserIdAndToken],
    metaclass=ABCMeta,
):
    pass


class IUserReaderRepository(
    IReader[
        User,
        Union[UserById, UserByNickname],
    ],
    metaclass=ABCMeta,
):
    pass


class IUserRepository(
    ICreator[User],
    IUserReaderRepository,
    IUpdater[User],
    IDeleter,
    metaclass=ABCMeta,
):
    pass
