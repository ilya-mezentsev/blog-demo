from typing import Mapping, Any

import sqlalchemy as sa  # type: ignore

from blog_demo_backend.db import get_table
from blog_demo_backend.shared import DBConnectionFn
from blog_demo_backend.domains.shared import IRepository, Id

from ..models import Article
from ..spec import ArticleById


__all__ = [
    'ArticleRepository',
]


article_table = get_table('article')


class ArticleRepository(IRepository[Article, ArticleById]):
    def __init__(
            self,
            connection_fn: DBConnectionFn,
    ) -> None:

        self._connection_fn = connection_fn

    def _make_create_mapping(self, model: Article) -> Mapping[sa.Column, Any]:
        return {
            article_table.c.uuid: model.id,
            article_table.c.author_id: model.author_id,
            article_table.c.title: model.title,
            article_table.c.description: model.description,
            article_table.c.created: model.created,
            article_table.c.modified: model.modified,
        }

    def _make_where_for_read(self, specification: ArticleById) -> sa.sql.ColumnElement:
        return article_table.c.uuid == specification.article_id

    def _model_from_row(self, article_row: Mapping[str, Any]) -> Article:
        return Article(
            id=article_row['uuid'],
            author_id=article_row['author_id'],
            title=article_row['title'],
            description=article_row['description'],
            created=article_row['created'],
            modified=article_row['modified'],
        )

    def _make_update_mapping(self, model: Article) -> Mapping[sa.Column, Any]:
        return {
            article_table.c.title: model.title,
            article_table.c.description: model.description,
            article_table.c.modified: model.modified,
        }

    def _make_where_for_update(self, model: Article) -> sa.sql.ColumnElement:
        return article_table.c.uuid == model.id

    def _make_where_for_delete(self, model_id: Id) -> sa.sql.ColumnElement:
        return article_table.c.uuid == model_id

    @property
    def _table(self) -> sa.Table:
        return article_table

    @property
    def _connect(self) -> DBConnectionFn:
        return self._connection_fn
