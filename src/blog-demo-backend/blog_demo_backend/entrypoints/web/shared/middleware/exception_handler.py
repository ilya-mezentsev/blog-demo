import logging
from typing import Callable, Awaitable

from aiohttp import web

from ..response import server_error, make_json_response


__all__ = [
    'exception_handler',
]


@web.middleware
async def exception_handler(
        request: web.Request,
        handler: Callable[[web.Request], Awaitable[web.StreamResponse]]
) -> web.StreamResponse:

    try:
        return await handler(request)
    except Exception as e:
        logging.exception(
            f'Failed to process {request.method.upper()} {request.path}. Unhandled exception: {e!r}'
        )

        return make_json_response(server_error('Unknown error'))
