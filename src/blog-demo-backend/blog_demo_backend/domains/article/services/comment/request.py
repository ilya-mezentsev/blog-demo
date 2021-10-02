from dataclasses import dataclass
from typing import Iterable

from blog_demo_backend.domains.article import Comment
from blog_demo_backend.domains.shared import (
    Requester,
    Id,
    CreateResponse,
    ReadResponse,
    UpdateResponse,
    DeleteResponse,
)


__all__ = [
    'GetCommentsRequest', 'GetCommentsResponse',
    'CreateCommentRequest', 'CreateCommentResponse',
    'UpdateCommentRequest', 'UpdateCommentResponse',
    'DeleteCommentRequest', 'DeleteCommentResponse',
]


@dataclass
class GetCommentsRequest(Requester):
    article_id: Id


@dataclass
class GetCommentsResponse(ReadResponse):
    comments: Iterable[Comment]


@dataclass
class CreateCommentRequest(Requester):
    article_id: Id
    text: str


@dataclass
class CreateCommentResponse(CreateResponse):
    comment: Comment


@dataclass
class UpdateCommentRequest(Requester):
    article_id: Id
    comment_id: Id
    text: str


@dataclass
class UpdateCommentResponse(UpdateResponse):
    comment: Comment


@dataclass
class DeleteCommentRequest(Requester):
    article_id: Id
    comment_id: Id


@dataclass
class DeleteCommentResponse(DeleteResponse):
    pass
