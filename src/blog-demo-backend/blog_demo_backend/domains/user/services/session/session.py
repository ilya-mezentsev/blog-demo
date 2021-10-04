from typing import Union, Optional

from blog_demo_backend.domains.user import UserSession
from blog_demo_backend.domains.shared import (
    ServiceError,
    NotFound,
)

from ...shared import create_hash
from ...spec import SessionByHash
from ...types import IUserSessionRepository

from .request import *


class UserSessionService:
    """
    Сервис для управления пользовательскими сессиями.
    """

    def __init__(
            self,
            session_repository: IUserSessionRepository,
    ) -> None:

        self._session_repository = session_repository

    async def create_session(
            self,
            request: CreateSessionRequest,
    ) -> Union[CreateSessionResponse, ServiceError]:

        session = await self._session_repository.read_one(SessionByHash(
            hash=create_hash(request.password),
        ))

        if session is not None:
            return CreateSessionResponse(session)
        else:
            return NotFound('user-not-found')

    async def get_session_by_token(
            self,
            token: str,
    ) -> Optional[UserSession]:

        return await self._session_repository.read_one(SessionByHash(
            hash=token,
        ))
