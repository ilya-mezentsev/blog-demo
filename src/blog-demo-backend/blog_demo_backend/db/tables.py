from sqlalchemy import (  # type: ignore
    MetaData,
    Table,
    Column,
    ForeignKey,
    Integer,
    VARCHAR,
    TEXT,
    DateTime,
    Enum,
    text,
    UniqueConstraint,
)


__all__ = [
    'blog_tables',
]


blog_tables = MetaData()

Table(
    'user', blog_tables,
    Column('id', Integer(), autoincrement=True),
    Column('uuid', VARCHAR(36), unique=True, primary_key=True),
    Column(
        'role',
        Enum(
            'user', 'moderator',
            name='user_role',
        ),
        nullable=False,
    ),
    Column('nickname', VARCHAR(64), unique=True, nullable=False),
    Column('created', DateTime, nullable=False, server_default=text('NOW()')),
    Column('modified', DateTime, nullable=False, server_default=text('NOW()')),
)

Table(
    'user_token', blog_tables,
    Column('id', Integer(), autoincrement=True),
    Column('user_id', VARCHAR(36), ForeignKey('user.uuid')),
    Column('token', VARCHAR(32)),
    UniqueConstraint('user_id', 'token'),
)

Table(
    'article', blog_tables,
    Column('id', Integer(), autoincrement=True),
    Column('uuid', VARCHAR(36), unique=True, primary_key=True),
    Column('author_id', VARCHAR(36), ForeignKey('user.uuid')),
    Column('title', VARCHAR(256), nullable=False),
    Column('description', VARCHAR(1024), nullable=False),
    Column('content', TEXT(), nullable=False),
    Column('created', DateTime, nullable=False, server_default=text('NOW()')),
    Column('modified', DateTime, nullable=False, server_default=text('NOW()')),
)

Table(
    'comment', blog_tables,
    Column('id', Integer(), autoincrement=True),
    Column('uuid', VARCHAR(36), unique=True, primary_key=True),
    Column('article_id', VARCHAR(36), ForeignKey('article.uuid')),
    Column('author_id', VARCHAR(36), ForeignKey('user.uuid')),
    Column('text', VARCHAR(2048), nullable=False),
    Column('created', DateTime, nullable=False, server_default=text('NOW()')),
    Column('modified', DateTime, nullable=False, server_default=text('NOW()')),
)
