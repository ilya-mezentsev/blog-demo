from aiohttp import web

from blog_demo_backend.domains import UserDomain


__all__ = [
    'UserEntrypoint',
]


class UserEntrypoint:

    def __init__(
            self,
            user_domain: UserDomain,
    ) -> None:

        self._user_domain = user_domain

    def make_entrypoint(self) -> web.Application:
        app = web.Application()

        app.add_routes([
            web.post(r'', self._create_user),
            web.get(r'/{user_id}', self._read_user),
            web.patch(r'', self._update_user),
            web.delete(r'/{user_id}', self._delete_user),
        ])

        return app

    async def _create_user(self, request: web.Request) -> web.Response:
        raise NotImplementedError()

    async def _read_user(self, request: web.Request) -> web.Response:
        raise NotImplementedError()

    async def _update_user(self, request: web.Request) -> web.Response:
        raise NotImplementedError()

    async def _delete_user(self, request: web.Request) -> web.Response:
        raise NotImplementedError()
