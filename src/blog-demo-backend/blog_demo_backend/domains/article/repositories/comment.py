from typing import (
    Union,
    Mapping,
    Any,
)

import sqlalchemy as sa  # type: ignore

from blog_demo_backend.db import get_table
from blog_demo_backend.domains.shared import IRepository, Id

from ..models import Comment
from ..spec import (
    CommentByIds,
    CommentsByArticleId,
)


__all__ = [
    'CommentRepository',
]


comment_table = get_table('comment')


class CommentRepository(
    IRepository[
        Comment,
        Union[CommentByIds, CommentsByArticleId],
    ]
):

    def _make_create_mapping(self, model: Comment) -> Mapping[sa.Column, Any]:
        return {
            comment_table.c.uuid: model.id,
            comment_table.c.article_id: model.article_id,
            comment_table.c.author_id: model.author_id,
            comment_table.c.text: model.text,
            comment_table.c.created: model.created,
            comment_table.c.modified: model.modified,
        }

    def _make_where_for_read(
            self,
            specification: Union[CommentByIds, CommentsByArticleId],
    ) -> sa.sql.ColumnElement:

        if isinstance(specification, CommentByIds):
            return sa.and_(
                comment_table.c.uuid == specification.comment_id,
                comment_table.c.article_id == specification.article_id,
            )

        elif isinstance(specification, CommentsByArticleId):
            return comment_table.c.article_id == specification.article_id

        else:
            raise RuntimeError(
                f'Unknown specification type: {type(specification)!r}')

    def _model_from_row(self, comment_row: Mapping[str, Any]) -> Comment:
        return Comment(
            id=comment_row['uuid'],
            article_id=comment_row['article_id'],
            author_id=comment_row['author_id'],
            text=comment_row['text'],
            created=comment_row['created'],
            modified=comment_row['modified'],
        )

    def _make_update_mapping(self, model: Comment) -> Mapping[sa.Column, Any]:
        return {
            comment_table.c.text: model.text,
            comment_table.c.modified: model.modified,
        }

    def _make_where_for_update(self, model: Comment) -> sa.sql.ColumnElement:
        return sa.and_(
            comment_table.c.uuid == model.id,
            comment_table.c.article_id == model.article_id,
        )

    def _make_where_for_delete(self, model_id: Id) -> sa.sql.ColumnElement:
        return comment_table.c.uuid == model_id

    @property
    def _table(self) -> sa.Table:
        return comment_table
