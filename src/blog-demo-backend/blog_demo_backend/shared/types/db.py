from typing import Callable, AsyncContextManager

from sqlalchemy.ext.asyncio import AsyncConnection  # type: ignore


__all__ = [
    'DBConnectionFn',
]


DBConnectionFn = Callable[[], AsyncContextManager[AsyncConnection]]
