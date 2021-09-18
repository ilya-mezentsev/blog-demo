import datetime
from dataclasses import dataclass

from blog_demo_backend.domains.shared import Id


__all__ = [
    'Comment',
]


@dataclass
class Comment:
    id: Id
    article_id: Id
    author_id: Id
    text: str
    created: datetime.datetime
    modified: datetime.datetime
