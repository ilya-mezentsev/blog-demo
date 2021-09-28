import asyncio
from typing import Tuple

from blog_demo_backend.db import make_db_connector, DBSettings
from blog_demo_backend.domains import (
    ArticleDomain,
    ArticleSettings,
    UserDomain,
    ServiceService,
    PermissionSettings,
)
from blog_demo_backend.entrypoints import start_web_entrypoint, WebEntrypointSettings
from blog_demo_backend.shared import DBConnectionFn


__all__ = [
    'main'
]


async def _make_db_connector() -> DBConnectionFn:
    return await make_db_connector(DBSettings(
        dialect='postgresql',
        driver='asyncpg',
        user='blog_demo',
        password='password',
        db_name='blog_demo',
        schema_name='blog_demo',
        host='localhost',
        port=5555,
        echo=True,
    ))


async def _make_articles_settings() -> ArticleSettings:
    return ArticleSettings(
        articles_root_path='/tmp',
    )


async def _make_permission_settings() -> PermissionSettings:
    return PermissionSettings(
        permission_resolver_url='http://localhost:8887',
        auth_token='some-token',
        request_timeout=5,
    )


async def _make_web_entrypoint_settings() -> WebEntrypointSettings:
    return WebEntrypointSettings(
        host='0.0.0.0',
        port=8888,
    )


async def _prepare_domains_and_settings() -> Tuple[
    ArticleDomain,
    UserDomain,
    WebEntrypointSettings,
]:
    db_connector = await _make_db_connector()
    permission_service = ServiceService(
        settings=(await _make_permission_settings())
    )

    article_domain = ArticleDomain(
        article_settings=(await _make_articles_settings()),
        connection_fn=db_connector,
        permission_service=permission_service
    )

    user_domain = UserDomain(
        connection_fn=db_connector,
        permission_service=permission_service,
    )

    return (
        article_domain,
        user_domain,
        await _make_web_entrypoint_settings()
    )


def main() -> None:
    article_domain, user_domain, web_entrypoint_settings = asyncio.get_event_loop().run_until_complete(
        _prepare_domains_and_settings()
    )

    start_web_entrypoint(
        article_domain=article_domain,
        user_domain=user_domain,
        settings=web_entrypoint_settings,
    )
