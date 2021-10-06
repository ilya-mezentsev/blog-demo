from aiohttp import web

from blog_demo_backend.domains import ArticleDomain, UserDomain

from .article import ArticleEntrypoint
from .session import UserSessionEntrypoint
from .user import UserEntrypoint
from .settings import WebEntrypointSettings

from .shared import exception_handler, user_id_from_cookie


__all__ = [
    'start_web_entrypoint',
]


def start_web_entrypoint(
        article_domain: ArticleDomain,
        user_domain: UserDomain,
        settings: WebEntrypointSettings,
) -> None:

    app = _make_app(
        article_domain=article_domain,
        user_domain=user_domain,
    )

    web.run_app(
        app=app,
        host=settings.host,
        port=settings.port,
    )


def _make_app(
        article_domain: ArticleDomain,
        user_domain: UserDomain,
) -> web.Application:

    app = web.Application(
        middlewares=[
            user_id_from_cookie(
                get_session_by_key=user_domain.session_service.get_session_by_key,
            ),
            exception_handler,
        ],
    )

    article_entrypoint = ArticleEntrypoint(article_domain)
    user_session_entrypoint = UserSessionEntrypoint(user_domain)
    user_entrypoint = UserEntrypoint(user_domain)

    app.add_subapp(
        prefix=r'/articles',
        subapp=article_entrypoint.make_app(),
    )
    app.add_subapp(
        prefix=r'/users',
        subapp=user_entrypoint.make_app(),
    )
    app.add_subapp(
        prefix=r'/session',
        subapp=user_session_entrypoint.make_app(),
    )

    return app
