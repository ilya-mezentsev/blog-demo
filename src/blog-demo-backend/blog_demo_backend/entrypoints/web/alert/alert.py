import logging

from aiohttp import web
from aiohttp_basicauth import BasicAuthMiddleware  # type: ignore

from ..settings import BasicAuthSettings


__all__ = [
    'AlertEntrypoint',
]


class AlertEntrypoint:

    def make_app(
            self,

            # Пока нужно только тут. Если потребуется где-то еще, то имеет смысл передавать сразу в middlewares
            basic_auth: BasicAuthSettings,
    ) -> web.Application:
        app = web.Application(
            middlewares=[
                BasicAuthMiddleware(
                    username=basic_auth.username,
                    password=basic_auth.password,
                ),
            ],
        )

        app.add_routes([
            web.post(r'', self._on_alert),
        ])

        return app

    @staticmethod
    async def _on_alert(request: web.Request) -> web.Response:
        """
        Пока просто логирование.
        Тут предполагается каким-то образом вызвать изменение версии политик доступа
        """

        logging.warning(f'Got alert request: {await request.json()}')

        return web.Response(
            status=200,
            text='Got alert!\n',
        )
