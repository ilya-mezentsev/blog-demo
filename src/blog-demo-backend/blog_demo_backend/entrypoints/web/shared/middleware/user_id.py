from typing import Callable, Awaitable, Optional

from aiohttp import web

from blog_demo_backend.domains.user import UserSession


__all__ = [
    'user_id_from_cookie',
]


def user_id_from_cookie(get_session_by_key: Callable[[str], Awaitable[Optional[UserSession]]]):

    @web.middleware
    async def _user_id_from_cookie(
            request: web.Request,
            handler: Callable[[web.Request], Awaitable[web.StreamResponse]],
    ) -> web.StreamResponse:

        session_key = request.cookies.get('BLOG_DEMO_SESSION_KEY', '')
        session = await get_session_by_key(session_key)

        user_id: Optional[str]
        if session is not None:
            user_id = session.user_id
        else:
            user_id = None

        request['context'] = {
            **request.get('context', {}),
            'user_id': user_id,
        }

        return await handler(request)

    return _user_id_from_cookie
