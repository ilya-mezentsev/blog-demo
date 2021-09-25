import asyncio
import uuid

from blog_demo_backend.db import (
    make_db_connector,
    DBSettings,
    get_table,
)


__all__ = [
    'main'
]


async def check_db() -> None:
    connector_fn = await make_db_connector(DBSettings(
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

    user_t = get_table('user')
    query = user_t.insert().values({
        'uuid': str(uuid.uuid4()),
        'nickname': 'foo-bar',
    })

    async with connector_fn() as conn:
        res = await conn.execute(query)
        user_id = res.inserted_primary_key[0]

    print(f'User with id {user_id} is created')


def main() -> None:
    asyncio.get_event_loop().run_until_complete(check_db())
