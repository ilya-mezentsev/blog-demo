from dataclasses import dataclass

from blog_demo_backend.domains.shared import Id, BaseSpec


__all__ = [
    'ArticleById',
]


@dataclass
class ArticleById(BaseSpec):
    article_id: Id
