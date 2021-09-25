from contextlib import asynccontextmanager
from functools import partial

import sqlalchemy  # type: ignore
from sqlalchemy.ext.asyncio import (  # type: ignore
    create_async_engine,
    AsyncConnection,
    AsyncEngine,
)

from blog_demo_backend.shared import DBConnectionFn

from .settings import DBSettings


__all__ = [
    'make_db_connector',
]


@asynccontextmanager
async def _connection_context_manager(
        settings: DBSettings,
        engine: AsyncEngine,
):

    connection: AsyncConnection = await engine.connect()
    await connection.execute(sqlalchemy.text(f'set search_path to {settings.schema_name}'))
    try:
        yield connection
    finally:
        await connection.commit()
        await connection.close()


async def make_db_connector(settings: DBSettings) -> DBConnectionFn:
    engine = create_async_engine(
        f'{settings.dialect}+{settings.driver}://'
        f'{settings.user}:{settings.password}@{settings.host}:{settings.port}/{settings.db_name}',

        echo=settings.echo,
    )

    return partial(
        _connection_context_manager,
        settings=settings,
        engine=engine,
    )
