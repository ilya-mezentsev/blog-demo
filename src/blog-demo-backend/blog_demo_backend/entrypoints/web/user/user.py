from typing import Iterable, Any

from aiohttp import web

from blog_demo_backend.domains.user import (
    UserDomain,
    GetUserRequest,
    UpdateUserRequest,
    DeleteUserRequest,
)

from ..shared import (
    from_response,
    make_json_response,
    read_json,
)


__all__ = [
    'UserEntrypoint',
]


class UserEntrypoint:

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
            web.get(r'/{user_id}', self._read_user),
            web.patch(r'/{user_id}', self._update_user),
            web.delete(r'/{user_id}', self._delete_user),
        ])

        return app

    async def _read_user(self, request: web.Request) -> web.Response:
        user_id = request.match_info['user_id']
        response_model = await self._user_domain.user_service.read(GetUserRequest(
            request_user_id=request['context']['user_id'],
            user_id=user_id,
        ))

        return make_json_response(from_response(response_model))

    async def _update_user(self, request: web.Request) -> web.Response:
        request_dict, invalid = await read_json(request)
        if invalid is not None:
            return make_json_response(from_response(invalid))

        assert request_dict is not None
        response_model = await self._user_domain.user_service.update(UpdateUserRequest(
            request_user_id=request['context']['user_id'],
            user_id=request.match_info['user_id'],
            nickname=request_dict.get('nickname', ''),
        ))

        return make_json_response(from_response(response_model))

    async def _delete_user(self, request: web.Request) -> web.Response:
        user_id = request.match_info['user_id']
        response_model = await self._user_domain.user_service.delete(DeleteUserRequest(
            request_user_id=request['context']['user_id'],
            user_id=user_id,
        ))

        return make_json_response(from_response(response_model))
