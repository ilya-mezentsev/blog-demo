import base64
import logging
from typing import Union, Optional

from blog_demo_backend.domains.user import UserSession
from blog_demo_backend.domains.shared import (
    ServiceError,
    NotFound,
)

from ...shared import create_hash
from ...spec import (
    SessionByUserIdAndToken,
    UserByNickname,
)
from ...types import IUserSessionRepository, IUserReaderRepository

from .request import *


class UserSessionService:
    """
    Сервис для управления пользовательскими сессиями.
    """

    def __init__(
            self,
            session_repository: IUserSessionRepository,
            user_repository: IUserReaderRepository,
    ) -> None:

        self._session_repository = session_repository
        self._user_repository = user_repository

    async def create_session(
            self,
            request: CreateSessionRequest,
    ) -> Union[CreateSessionResponse, ServiceError]:

        user = await self._user_repository.read_one(UserByNickname(
            nickname=request.nickname,
        ))
        if user is None:
            return NotFound('user-not-found')

        session = await self._session_repository.read_one(SessionByUserIdAndToken(
            user_id=user.id,
            token=create_hash(request.password),
        ))

        if session is not None:
            session_hash = base64.b64encode(
                f'{session.user_id}:{session.token}'.encode('utf-8'))
            return CreateSessionResponse(
                session_key=session_hash.decode('utf-8'),
            )
        else:
            return NotFound('user-not-found')

    async def get_session_by_key(
            self,
            session_hash: str,
    ) -> Optional[UserSession]:

        user_id: Optional[str] = None
        token: Optional[str] = None

        try:
            session_hash_parts = base64. \
                b64decode(session_hash). \
                decode('utf-8'). \
                split(':')
            if len(session_hash_parts) > 1:
                user_id, token = session_hash_parts[0], session_hash_parts[1]
        except Exception as e:
            logging.exception(f'Failed to decode session_hash: {e!r}')
            return None

        return await self._session_repository.read_one(SessionByUserIdAndToken(
            user_id=user_id or '',
            token=token or '',
        ))
