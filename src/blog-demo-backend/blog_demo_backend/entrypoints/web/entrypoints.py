from aiohttp import web

from blog_demo_backend.domains import ArticleDomain, UserDomain

from .article import ArticleEntrypoint
from .user import UserEntrypoint
from .settings import WebEntrypointSettings

from .shared import exception_handler


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
            exception_handler,
        ],
    )

    article_entrypoint = ArticleEntrypoint(article_domain)
    user_entrypoint = UserEntrypoint(user_domain)

    app.add_subapp(r'/articles', article_entrypoint.make_entrypoint())
    app.add_subapp(r'/users', user_entrypoint.make_entrypoint())

    return app
