from typing import Union, Optional

from blog_demo_backend.domains.user import UserSession
from blog_demo_backend.domains.shared import (
    IReader,
    ServiceError,
    NotFound,
)

from ...spec import SessionByHash
from ...shared import create_hash

from .request import *


class UserSessionService:
    """
    Сервис для управления пользовательскими сессиями.
    """

    def __init__(
            self,
            session_repository: IReader[UserSession, SessionByHash],
    ) -> None:

        self._session_repository = session_repository

    async def create_session(
            self,
            request: CreateSessionRequest,
    ) -> Union[CreateSessionResponse, ServiceError]:

        session = self._session_repository.read(SessionByHash(
            hash=create_hash(
                nickname=request.nickname,
                password=request.password,
            ),
        ))

        if isinstance(session, UserSession):
            return CreateSessionResponse(session)
        else:
            return NotFound('user-not-found')

    async def get_session_by_token(
            self,
            token: str,
    ) -> Optional[UserSession]:

        session = self._session_repository.read(SessionByHash(
            hash=token,
        ))

        if isinstance(session, UserSession):
            return session
        else:
            return None
