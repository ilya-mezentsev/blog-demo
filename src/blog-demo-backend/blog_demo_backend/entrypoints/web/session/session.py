from typing import Iterable, Any

from aiohttp import web

from blog_demo_backend.domains.user import UserDomain, CreateSessionRequest

from ..shared import (
    from_response,
    session_response,
    make_json_response,
    read_json,
)


__all__ = [
    'UserSessionEntrypoint',
]


class UserSessionEntrypoint:

    def __init__(
            self,
            user_domain: UserDomain,
    ) -> None:

        self._user_domain = user_domain

    def make_app(self, middlewares: Iterable[Any]) -> web.Application:
        app = web.Application(
            middlewares=middlewares,
        )

        app.add_routes([
            web.post(r'', self.create_session),
        ])

        return app

    async def create_session(self, request: web.Request) -> web.Response:
        request_dict, invalid = await read_json(request)
        if invalid is not None:
            return make_json_response(from_response(invalid))

        assert request_dict is not None
        response_model = await self._user_domain.session_service.create_session(CreateSessionRequest(
            nickname=request_dict.get('nickname', ''),
            password=request_dict.get('password', ''),
        ))

        return make_json_response(session_response(response_model))
