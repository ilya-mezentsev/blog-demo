from dataclasses import dataclass

from blog_demo_backend.domains.shared import Id


__all__ = [
    'ArticleById',
]


@dataclass
class ArticleById:
    article_id: Id
