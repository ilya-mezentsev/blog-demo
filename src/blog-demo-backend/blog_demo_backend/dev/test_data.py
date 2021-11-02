import datetime
import glob
import os.path
from typing import Sequence
from uuid import uuid4

import asyncio

import lorem  # type: ignore

from blog_demo_backend.db import make_db_connector
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
    MemoryCacheRepository,
)
from blog_demo_backend.settings import Config


__all__ = [
    'init_test_data',
]


async def init_test_data(config: Config) -> None:

    db_connector = await make_db_connector(config.db_settings())

    users = await _init_users(
        user_repository=UserRepository(db_connector, MemoryCacheRepository()),
        session_repository=UserSessionRepository(
            db_connector, MemoryCacheRepository()),
    )

    await _init_articles(
        users=users,
        article_repository=ArticleRepository(
            db_connector, MemoryCacheRepository()),
        comment_repository=CommentRepository(
            db_connector, MemoryCacheRepository()),
        articles_root_path=config.article_settings().articles_root_path,
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
        for i in range(0, 100)
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
        for i in range(0, 10)
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
        articles_root_path: str,
) -> None:

    now = datetime.datetime.now()

    articles = []
    comments = []

    # Первым десяти пользователям добавим в авторство по 10 статей
    for user_index in range(0, 10):
        for _ in range(0, 10):
            articles.append(_make_article(
                author_id=users[user_index].id,
                now=now,
            ))

    # Следующей десятке добавим в авторство по 20 статей
    for user_index in range(10, 20):
        for _ in range(0, 20):
            articles.append(_make_article(
                author_id=users[user_index].id,
                now=now,
            ))

    # Третий десяток получает по 30 статей в авторство
    for user_index in range(20, 30):
        for _ in range(0, 30):
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

    article_db_creation_coroutines = [
        article_repository.create(article)
        for article in articles
    ]
    article_fs_creation_coroutines = [
        _create_article_file(
            article_filename=article.id,
            articles_root_path=articles_root_path,
        )
        for article in articles
    ]
    comment_creation_coroutines = [
        comment_repository.create(comment)
        for comment in comments
    ]

    await _check_articles_path(articles_root_path)
    await asyncio.gather(*article_db_creation_coroutines)
    await asyncio.gather(*article_fs_creation_coroutines)
    await _create_articles_for_tests(articles_root_path)
    await asyncio.gather(*comment_creation_coroutines)


def _make_article(author_id: Id, now: datetime.datetime) -> Article:
    return Article(
        id=str(uuid4()),
        author_id=author_id,
        title=lorem.sentence(),
        description=lorem.paragraph(),
        created=now,
        modified=now,
    )


async def _check_articles_path(articles_root_path: str) -> None:
    if not os.path.exists(articles_root_path):
        os.mkdir(
            path=articles_root_path,
            mode=0o777,
        )
    else:
        files = glob.glob(os.path.join(articles_root_path, '*'))
        for file in files:
            os.remove(file)


async def _create_article_file(
        article_filename: str,
        articles_root_path: str,
) -> None:

    assert os.path.exists(articles_root_path)

    content = ''
    for _ in range(0, 3):
        content += f'{lorem.text()}\n\n'

    with open(os.path.join(
        articles_root_path,
        article_filename,
    ), 'w') as f:
        f.write(content)


async def _create_articles_for_tests(articles_root_path: str) -> None:
    """
    В данной функции создаем файлики,
    которые будут использоваться для создания статей в процессе нагрузочного тестирования
    """

    article_for_test_creation_coroutines = [
        _create_article_file(
            article_filename=f'for_test_{i}.txt',
            articles_root_path=articles_root_path,
        )
        for i in range(0, 10)
    ]

    await asyncio.gather(*article_for_test_creation_coroutines)
