import datetime
from typing import Union, Optional
from uuid import uuid4

from blog_demo_backend.domains.user import UserSession, User
from blog_demo_backend.domains.shared import (
    IRepository,
    ServiceError,
    NotFound,
    InvalidRequest,
)

from ...shared import create_hash
from ...spec import SessionByHash, UserByNickname, UserById
from ...types import IUserSessionRepository

from .request import *


class UserSessionService:
    """
    Сервис для управления пользовательскими сессиями.
    """

    def __init__(
            self,
            user_repository: IRepository[User, Union[UserById, UserByNickname]],
            session_repository: IUserSessionRepository,
    ) -> None:

        self._user_repository = user_repository
        self._session_repository = session_repository

    async def create_user(
            self,
            request: CreateUserRequest,
    ) -> Union[CreateUserResponse, ServiceError]:

        user_with_nickname = await self._user_repository.read(UserByNickname(
            nickname=request.nickname,
        ))
        if user_with_nickname is not None:
            return InvalidRequest(
                description='user-already-exists',
            )

        model = User(
            id=str(uuid4()),
            nickname=request.nickname,
            role='user',
            created=datetime.datetime.now(),
            modified=datetime.datetime.now(),
        )
        await self._user_repository.create(model)
        await self._session_repository.create(UserSession(
            user_id=model.id,
            token=create_hash(
                nickname=request.nickname,
                password=request.password,
            ),
        ))

        return CreateUserResponse(model)

    async def create_session(
            self,
            request: CreateSessionRequest,
    ) -> Union[CreateSessionResponse, ServiceError]:

        session = await self._session_repository.read(SessionByHash(
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
