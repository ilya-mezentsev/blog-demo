from dataclasses import dataclass

from blog_demo_backend.domains.shared import Id, BaseSpec


__all__ = [
    'CommentByIds',
    'CommentsByArticleId',
]


@dataclass
class CommentByIds(BaseSpec):
    article_id: Id
    comment_id: Id


@dataclass
class CommentsByArticleId(BaseSpec):
    article_id: Id
