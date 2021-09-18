from dataclasses import dataclass

from blog_demo_backend.domains.shared import Requester


__all__ = [
    'GetCommentsRequest', 'GetCommentsResponse',
    'CreateCommentRequest', 'CreateCommentResponse',
    'UpdateCommentRequest', 'UpdateCommentResponse',
    'DeleteCommentRequest', 'DeleteCommentResponse',
]


@dataclass
class GetCommentsRequest(Requester):
    ...


@dataclass
class GetCommentsResponse:
    ...


@dataclass
class CreateCommentRequest(Requester):
    ...


@dataclass
class CreateCommentResponse:
    ...


@dataclass
class UpdateCommentRequest(Requester):
    ...


@dataclass
class UpdateCommentResponse:
    ...


@dataclass
class DeleteCommentRequest(Requester):
    ...


@dataclass
class DeleteCommentResponse:
    ...
