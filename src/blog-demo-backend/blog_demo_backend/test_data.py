import asyncio
import time

from blog_demo_backend import dev
from blog_demo_backend.settings import cli_arguments, Config


__all__ = [
    'init_test_data',
]


def init_test_data() -> None:
    start_ts = time.time()
    args = cli_arguments()
    config = Config(args.config_path)

    asyncio.get_event_loop().run_until_complete(
        dev.init_test_data(config),
    )

    print(f'Test data init took: {time.time() - start_ts}')
