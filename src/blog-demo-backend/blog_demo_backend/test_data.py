import asyncio
import time
from typing import Awaitable, Callable

from blog_demo_backend import dev
from blog_demo_backend.settings import cli_arguments, Config


__all__ = [
    'init_test_data',
    'reset_schema',
]


def init_test_data() -> None:
    _exec(
        fn=dev.init_test_data,
        process_name='Test data init',
    )


def reset_schema() -> None:
    _exec(
        fn=dev.reset_schema,
        process_name='Reset schema',
    )


def _exec(
        fn: Callable[[Config], Awaitable[None]],
        process_name: str,
) -> None:
    start_ts = time.time()
    args = cli_arguments()
    config = Config(args.config_path)

    asyncio.get_event_loop().run_until_complete(
        fn(config),
    )

    print(f'{process_name} took: {time.time() - start_ts} second(s)')
