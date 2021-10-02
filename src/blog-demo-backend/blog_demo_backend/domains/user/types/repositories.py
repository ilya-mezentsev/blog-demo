from abc import ABCMeta

from blog_demo_backend.domains.shared import (
    ICreator,
    IReader,
)
from blog_demo_backend.domains.user import UserSession

from ..spec import SessionByHash


__all__ = [
    'IUserSessionRepository',
]


class IUserSessionRepository(
    ICreator[UserSession],
    IReader[UserSession, SessionByHash],
    metaclass=ABCMeta
):
    pass
