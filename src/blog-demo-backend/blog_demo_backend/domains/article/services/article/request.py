from dataclasses import dataclass
from typing import Iterable, Optional

from blog_demo_backend.domains.article import Article
from blog_demo_backend.domains.shared import (
    Requester,
    Id,
    CreateResponse,
    ReadResponse,
    UpdateResponse,
    DeleteResponse,
)


__all__ = [
    'GetArticlesRequest', 'GetArticlesResponse',
    'GetArticleRequest', 'GetArticleResponse',
    'CreateArticleRequest', 'CreateArticleResponse',
    'UpdateArticleRequest', 'UpdateArticleResponse',
    'DeleteArticleRequest', 'DeleteArticleResponse',
]


@dataclass
class GetArticlesRequest(Requester):
    pass


@dataclass
class GetArticlesResponse(ReadResponse):
    articles: Iterable[Article]


@dataclass
class GetArticleRequest(Requester):
    article_id: Id


@dataclass
class GetArticleResponse(ReadResponse):
    article: Article


@dataclass
class CreateArticleRequest(Requester):
    title: str
    description: str
    content: str


@dataclass
class CreateArticleResponse(CreateResponse):
    article: Article


@dataclass
class UpdateArticleRequest(Requester):
    article_id: Id
    title: str
    description: str
    content: Optional[str]


@dataclass
class UpdateArticleResponse(UpdateResponse):
    article: Article


@dataclass
class DeleteArticleRequest(Requester):
    article_id: Id


@dataclass
class DeleteArticleResponse(DeleteResponse):
    pass
