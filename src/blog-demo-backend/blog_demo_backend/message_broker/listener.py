from typing import Iterable, Union

import asyncio
import aioredis
import async_timeout

from blog_demo_backend.domains import UserDomain, ArticleDomain

from .const import RESET_CACHE_CHANNEL


__all__ = [
    'listen_redis_messages',
]


async def listen_redis_messages(
        redis: aioredis.Redis,
        domains: Iterable[Union[
            UserDomain,
            ArticleDomain,
        ]],
) -> None:

    channel = redis.pubsub()
    await channel.subscribe(RESET_CACHE_CHANNEL)

    while True:
        try:
            async with async_timeout.timeout(1):
                message = await channel.get_message(ignore_subscribe_messages=True)

                if (
                        message is not None and
                        message['channel'].decode() == RESET_CACHE_CHANNEL
                ):
                    await _on_reset_cache_message(
                        entity_type=message['data'].decode(),
                        domains=domains,
                    )

                await asyncio.sleep(0.01)
        except asyncio.TimeoutError:
            pass


async def _on_reset_cache_message(
        entity_type: str,
        domains: Iterable[Union[
            UserDomain,
            ArticleDomain,
        ]],
) -> None:

    for domain in domains:
        await domain.on_cache_changed(
            entity_type=entity_type,
        )
