import datetime
from typing import Sequence
from uuid import uuid4

import asyncio
import lorem  # type: ignore

from sqlalchemy import (  # type: ignore
    exists,
    select,
    text,
)
from sqlalchemy.schema import DropSchema, CreateSchema  # type: ignore

from blog_demo_backend.db import make_db_connector, blog_tables
from blog_demo_backend.domains import (
    ArticleRepository,
    CommentRepository,
    UserRepository,
    UserSessionRepository,
    User,
    UserSession,
    create_hash,
    Article,
    Comment,
    Id,
    CacheMiss,
)
from blog_demo_backend.settings import Config


__all__ = [
    'init_test_data',
    'reset_schema',
]


async def reset_schema(config: Config) -> None:
    db_settings = config.db_settings()
    db_connector = await make_db_connector(db_settings)

    q = select(
        exists(
            select([
                text('schema_name'),
            ]).
            select_from(text('information_schema.schemata')).
            where(text(f'schema_name = \'{db_settings.schema_name}\''))
        )
    )

    async with db_connector() as conn:
        if (await conn.execute(q)).scalar():
            await conn.execute(DropSchema(
                name=db_settings.schema_name,
                cascade=True,
            ))

        await conn.execute(CreateSchema(db_settings.schema_name))

        await conn.run_sync(blog_tables.drop_all)
        await conn.run_sync(blog_tables.create_all)


async def init_test_data(config: Config) -> None:

    db_connector = await make_db_connector(config.db_settings())

    users = await _init_users(
        user_repository=UserRepository(db_connector, CacheMiss()),
        session_repository=UserSessionRepository(db_connector, CacheMiss()),
    )

    await _init_articles(
        users=users,
        article_repository=ArticleRepository(db_connector, CacheMiss()),
        comment_repository=CommentRepository(db_connector, CacheMiss()),
    )


async def _init_users(
        user_repository: UserRepository,
        session_repository: UserSessionRepository,
) -> Sequence[User]:

    now = datetime.datetime.now()
    users = [
        User(
            id=str(uuid4()),
            role='user',
            nickname=f'user_{i}',
            created=now,
            modified=now,
        )
        for i in range(100)
    ]

    user_creation_coroutines = [
        user_repository.create(user)
        for user in users
    ]
    await asyncio.gather(*user_creation_coroutines)

    # Модераторов лучше создать отдельно (для простоты)
    # Заметка. На текущий момент штатного метода создания модераторов нет,
    # т.к. не особо нужно в рамках демки
    moderators = [
        User(
            id=str(uuid4()),
            role='moderator',
            nickname=f'moderator_{i}',
            created=now,
            modified=now,
        )
        for i in range(10)
    ]

    moderator_creation_coroutines = [
        user_repository.create(moderator)
        for moderator in moderators
    ]
    await asyncio.gather(*moderator_creation_coroutines)

    users_sessions = [
        UserSession(
            user_id=user.id,
            token=create_hash('password'),
        )
        for user in users + moderators
    ]

    user_session_creation_coroutines = [
        session_repository.create(user_session)
        for user_session in users_sessions
    ]
    await asyncio.gather(*user_session_creation_coroutines)

    return users


async def _init_articles(
        users: Sequence[User],
        article_repository: ArticleRepository,
        comment_repository: CommentRepository,
) -> None:

    now = datetime.datetime.now()

    articles = []
    comments = []

    # Первым десяти пользователям добавим в авторство по 10 статей
    for user_index in range(10):
        for _ in range(10):
            articles.append(_make_article(
                author_id=users[user_index].id,
                now=now,
            ))

    # Следующей десятке добавим в авторство по 20 статей
    for user_index in range(10, 20):
        for _ in range(20):
            articles.append(_make_article(
                author_id=users[user_index].id,
                now=now,
            ))

    # Третий десяток получает по 30 статей в авторство
    for user_index in range(20, 30):
        for _ in range(30):
            articles.append(_make_article(
                author_id=users[user_index].id,
                now=now,
            ))

    # Каждый пользователь оставляет по одному комменту к каждой статье
    for user in users:
        for article in articles:
            comments.append(Comment(
                id=str(uuid4()),
                article_id=article.id,
                author_id=user.id,
                text=lorem.paragraph(),
                created=now,
                modified=now,
            ))

    article_creation_coroutines = [
        article_repository.create(article)
        for article in articles
    ]
    comment_creation_coroutines = [
        comment_repository.create(comment)
        for comment in comments
    ]

    await asyncio.gather(*article_creation_coroutines)
    await asyncio.gather(*comment_creation_coroutines)


def _make_article(author_id: Id, now: datetime.datetime) -> Article:
    return Article(
        id=str(uuid4()),
        author_id=author_id,
        title=lorem.sentence(),
        description=lorem.paragraph(),
        content='\n\n'.join(lorem.paragraph() for _ in range(3)),
        created=now,
        modified=now,
    )
