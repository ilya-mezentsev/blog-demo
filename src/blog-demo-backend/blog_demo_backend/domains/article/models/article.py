import datetime
from dataclasses import dataclass

from blog_demo_backend.domains.shared import Id


__all__ = [
    'Article',
]


@dataclass
class Article:
    id: Id
    author_id: Id
    title: str
    description: str
    content: str
    created: datetime.datetime
    modified: datetime.datetime
