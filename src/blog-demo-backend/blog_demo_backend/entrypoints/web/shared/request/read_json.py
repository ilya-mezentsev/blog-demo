import logging
from typing import (
    Tuple,
    Optional,
    Mapping,
    Any,
)

from aiohttp import web

from blog_demo_backend.domains.shared import InvalidRequest


__all__ = [
    'read_json',
]


async def read_json(request: web.Request) -> Tuple[
    Optional[Mapping[str, Any]],
    Optional[InvalidRequest],
]:

    try:
        return await request.json(), None
    except Exception as e:
        logging.exception(f'Unable to unmarshal request json {e!r}: {(await request.text())[:256]!r}')

        return None, InvalidRequest(
            description='invalid-json',
        )
