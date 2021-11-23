from typing import Tuple

import aioredis

from blog_demo_backend.domains import (
    MemoryCache,
    CacheFactoryFn,
)

from .const import RESET_CACHE_CHANNEL
from .settings import MessageBrokerConfig


__all__ = [
    'make_broker_and_cache_factory',
]


def make_broker_and_cache_factory(config: MessageBrokerConfig) -> Tuple[
    aioredis.Redis,
    CacheFactoryFn,
]:
    redis = aioredis.from_url(f'redis://{config.host}')

    return (
        redis,
        lambda entity_type: MemoryCache(
            reset_cache_channel=RESET_CACHE_CHANNEL,
            entity_type=entity_type,
            redis=redis,
        )
    )
