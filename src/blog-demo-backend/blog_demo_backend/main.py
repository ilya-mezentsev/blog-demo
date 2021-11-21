from typing import Tuple

import asyncio
import aioredis

from blog_demo_backend.db import make_db_connector
from blog_demo_backend.domains import (
    ArticleDomain,
    UserDomain,
    PermissionService,
)
from blog_demo_backend.entrypoints import start_web_entrypoint
from blog_demo_backend.message_broker import (
    make_broker_and_cache_factory,
    listen_redis_messages,
)
from blog_demo_backend.settings import cli_arguments, Config

from .logs import configure_logging


__all__ = [
    'main',
]


async def _prepare_domains_and_settings(
        config: Config,
        permission_service: PermissionService,
) -> Tuple[
    ArticleDomain,
    UserDomain,
    aioredis.Redis
]:

    redis, cache_factory_fn = make_broker_and_cache_factory(
        config=config.message_broker(),
    )

    db_connector = await make_db_connector(config.db_settings())

    user_domain = UserDomain(
        cache_factory_fn=cache_factory_fn,
        connection_fn=db_connector,
        permission_service=permission_service,
    )

    article_domain = ArticleDomain(
        cache_factory_fn=cache_factory_fn,
        connection_fn=db_connector,
        permission_service=permission_service,
        user_role_repository=user_domain.user_role_repository,
    )

    return (
        article_domain,
        user_domain,
        redis,
    )


def main() -> None:
    args = cli_arguments()

    configure_logging(args.logging_level)

    config = Config(args.config_path)

    permission_service = PermissionService(
        settings=config.permission_settings()
    )

    article_domain, user_domain, redis = asyncio.get_event_loop().run_until_complete(
        _prepare_domains_and_settings(
            permission_service=permission_service,
            config=config,
        ),
    )

    asyncio.get_event_loop().create_task(listen_redis_messages(
        redis=redis,
        domains=[
            article_domain,
            user_domain,
        ],
    ))

    start_web_entrypoint(
        article_domain=article_domain,
        user_domain=user_domain,
        permission_service=permission_service,
        settings=config.web_entrypoint_settings(),
    )
