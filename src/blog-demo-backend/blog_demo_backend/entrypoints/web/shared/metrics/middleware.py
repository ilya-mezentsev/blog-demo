import time
from typing import Callable, Awaitable

from aiohttp import web


def prom_middleware(app_name: str):

    @web.middleware
    async def middleware_handler(
            request: web.Request,
            handler: Callable[[web.Request], Awaitable[web.StreamResponse]],
    ) -> web.StreamResponse:
        request['start_time'] = time.time()
        response = await handler(request)
        resp_time = time.time() - request['start_time']

        request.app['REQUEST_TIME']. \
            labels(app_name, request.path). \
            observe(resp_time)

        return response

    return middleware_handler
