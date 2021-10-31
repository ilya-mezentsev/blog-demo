from aiohttp import web
from aiohttp_basicauth import BasicAuthMiddleware  # type: ignore

from blog_demo_backend.domains import PermissionService

from ..settings import BasicAuthSettings


__all__ = [
    'AlertEntrypoint',
]


class AlertEntrypoint:

    def __init__(
            self,
            permission_service: PermissionService,
    ) -> None:

        self._permission_service = permission_service

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

    async def _on_alert(self, request: web.Request) -> web.Response:
        alert_data = await request.json()
        for alert in alert_data.get('alerts', []):
            request_latency_seconds = alert.get(
                'annotations', {}).get('request_latency_seconds', 0)
            await self._permission_service.update_version(float(request_latency_seconds))

        return web.Response(
            status=200,
            text='Got alert!\n',
        )
