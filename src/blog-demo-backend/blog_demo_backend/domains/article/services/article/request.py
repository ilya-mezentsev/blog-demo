from dataclasses import dataclass

from blog_demo_backend.domains.shared import Requester


__all__ = [
    'GetArticlesRequest', 'GetArticlesResponse',
    'GetArticleRequest', 'GetArticleResponse',
    'CreateArticleRequest', 'CreateArticleResponse',
    'UpdateArticleRequest', 'UpdateArticleResponse',
    'DeleteArticleRequest', 'DeleteArticleResponse',
]


@dataclass
class GetArticlesRequest(Requester):
    ...


@dataclass
class GetArticlesResponse:
    ...


@dataclass
class GetArticleRequest(Requester):
    ...


@dataclass
class GetArticleResponse:
    ...


@dataclass
class CreateArticleRequest(Requester):
    ...


@dataclass
class CreateArticleResponse:
    ...


@dataclass
class UpdateArticleRequest(Requester):
    ...


@dataclass
class UpdateArticleResponse:
    ...


@dataclass
class DeleteArticleRequest(Requester):
    ...


@dataclass
class DeleteArticleResponse:
    ...
