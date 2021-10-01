import asyncio
from typing import Tuple

from blog_demo_backend.db import make_db_connector, DBSettings
from blog_demo_backend.domains import (
    ArticleDomain,
    UserDomain,
    PermissionService,
    UserRoleRepository,
)
from blog_demo_backend.entrypoints import start_web_entrypoint
from blog_demo_backend.settings import cli_arguments, Config
from blog_demo_backend.shared import DBConnectionFn

from .logs import configure_logging


__all__ = [
    'main'
]


async def _make_db_connector(s: DBSettings) -> DBConnectionFn:
    return await make_db_connector(s)


async def _prepare_domains_and_settings(config: Config) -> Tuple[
    ArticleDomain,
    UserDomain,
]:
    db_connector = await _make_db_connector(config.db_settings())
    permission_service = PermissionService(
        settings=config.permission_settings()
    )
    user_role_repository = UserRoleRepository(db_connector)

    article_domain = ArticleDomain(
        article_settings=config.article_settings(),
        connection_fn=db_connector,
        permission_service=permission_service,
        user_role_repository=user_role_repository,
    )

    user_domain = UserDomain(
        connection_fn=db_connector,
        permission_service=permission_service,
        user_role_repository=user_role_repository,
    )

    return (
        article_domain,
        user_domain,
    )


def main() -> None:
    args = cli_arguments()

    configure_logging(args.logging_level)

    config = Config(args.config_path)

    article_domain, user_domain = asyncio.get_event_loop().run_until_complete(
        _prepare_domains_and_settings(config)
    )

    start_web_entrypoint(
        article_domain=article_domain,
        user_domain=user_domain,
        settings=config.web_entrypoint_settings(),
    )
