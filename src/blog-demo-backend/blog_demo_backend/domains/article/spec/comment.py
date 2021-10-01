from dataclasses import dataclass

from blog_demo_backend.domains.shared import Id


__all__ = [
    'CommentByIds',
    'CommentsByArticleId',
]


@dataclass
class CommentByIds:
    article_id: Id
    comment_id: Id


@dataclass
class CommentsByArticleId:
    article_id: Id
