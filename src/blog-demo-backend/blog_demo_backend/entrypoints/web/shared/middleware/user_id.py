from typing import Callable, Awaitable

from aiohttp import web

from ..response import unauthorized_error, make_json_response


__all__ = [
    'user_id_from_cookie',
]


@web.middleware
async def user_id_from_cookie(
        request: web.Request,
        handler: Callable[[web.Request], Awaitable[web.StreamResponse]]
) -> web.StreamResponse:

    # todo id -> token
    user_id = request.cookies.get('BLOG_DEMO_USER_ID')

    if user_id is not None:
        request['context'] = {
            **request.get('context', {}),
            'user_id': user_id,
        }

        return await handler(request)

    else:
        return make_json_response(unauthorized_error(
            description='Auth cookie missed',
        ))
