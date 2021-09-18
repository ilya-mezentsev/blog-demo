from dataclasses import dataclass


__all__ = [
    'ArticleSettings',
]


@dataclass
class ArticleSettings:
    articles_root_path: str
