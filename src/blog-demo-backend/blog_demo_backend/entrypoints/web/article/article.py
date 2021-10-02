from typing import (
    Optional,
    Iterable,
    Any,
)

from aiohttp import web, web_request

from blog_demo_backend.domains.shared import InvalidRequest
from blog_demo_backend.domains.article import (
    ArticleDomain,
    CreateArticleRequest,
    GetArticlesRequest,
    GetArticleRequest,
    UpdateArticleRequest,
    DeleteArticleRequest,
    CreateCommentRequest,
    GetCommentsRequest,
    UpdateCommentRequest,
    DeleteCommentRequest,
)

from ..shared import (
    from_response,
    make_json_response,
    read_json,
)


__all__ = [
    'ArticleEntrypoint',
]


class ArticleEntrypoint:

    def __init__(
            self,
            article_domain: ArticleDomain
    ) -> None:

        self._article_domain = article_domain

    def make_app(self, middlewares: Iterable[Any]) -> web.Application:
        app = web.Application(
            middlewares=middlewares,
        )

        app.add_routes([
            web.post(r'', self._create_article),
            web.get(r'', self._read_articles),
            web.get(r'/{article_id}', self._read_article),
            web.patch(r'/{article_id}', self._update_article),
            web.delete(r'/{article_id}', self._delete_article),

            web.post(r'/{article_id}/comments', self._create_comment),
            web.get(r'/{article_id}/comments', self._read_comments),
            web.patch(
                r'/{article_id}/comments/{comment_id}',
                self._update_comment,
            ),
            web.delete(
                r'/{article_id}/comments/{comment_id}',
                self._delete_comment,
            ),
        ])

        return app

    async def _create_article(self, request: web.Request) -> web.Response:
        data = await request.post()
        file_fields = data.get('article_file')
        if not isinstance(file_fields, web_request.FileField):
            return make_json_response(from_response(InvalidRequest(
                description='missed-file',
            )))

        title = data.get('title', '')
        description = data.get('description', '')

        response_model = await self._article_domain.article_service.create(CreateArticleRequest(
            request_user_id=request['context']['user_id'],
            author_id=request['context']['user_id'],
            title=title if isinstance(title, str) else '',
            description=description if isinstance(description, str) else '',
            content=file_fields.file.read(),
        ))

        return make_json_response(from_response(response_model))

    async def _read_articles(self, request: web.Request) -> web.Response:
        response_model = await self._article_domain.article_service.read(GetArticlesRequest(
            request_user_id=request['context']['user_id'],
        ))

        return make_json_response(from_response(response_model))

    async def _read_article(self, request: web.Request) -> web.Response:
        article_id = request.match_info['article_id']
        response_model = await self._article_domain.article_service.read(GetArticleRequest(
            request_user_id=request['context']['user_id'],
            article_id=article_id,
        ))

        return make_json_response(from_response(response_model))

    async def _update_article(self, request: web.Request) -> web.Response:
        data = await request.post()
        file_fields = data.get('article_file')
        title = data.get('title', '')
        description = data.get('description', '')

        content: Optional[bytes]
        if isinstance(file_fields, web_request.FileField):
            content = file_fields.file.read()
        else:
            content = None

        response_model = await self._article_domain.article_service.update(UpdateArticleRequest(
            request_user_id=request['context']['user_id'],
            article_id=request.match_info['article_id'],
            title=title if isinstance(title, str) else '',
            description=description if isinstance(description, str) else '',
            content=content,
        ))

        return make_json_response(from_response(response_model))

    async def _delete_article(self, request: web.Request) -> web.Response:
        article_id = request.match_info['article_id']
        response_model = await self._article_domain.article_service.delete(DeleteArticleRequest(
            request_user_id=request['context']['user_id'],
            article_id=article_id,
        ))

        return make_json_response(from_response(response_model))

    async def _create_comment(self, request: web.Request) -> web.Response:
        request_dict, invalid = await read_json(request)
        if invalid is not None:
            return make_json_response(from_response(invalid))

        assert request_dict is not None
        response_model = await self._article_domain.comment_service.create(CreateCommentRequest(
            request_user_id=request['context']['user_id'],
            article_id=request.match_info['article_id'],
            author_id=request['context']['user_id'],
            text=request_dict.get('text', ''),
        ))

        return make_json_response(from_response(response_model))

    async def _read_comments(self, request: web.Request) -> web.Response:
        article_id = request.match_info['article_id']
        response_model = await self._article_domain.comment_service.read(GetCommentsRequest(
            request_user_id=request['context']['user_id'],
            article_id=article_id,
        ))

        return make_json_response(from_response(response_model))

    async def _update_comment(self, request: web.Request) -> web.Response:
        request_dict, invalid = await read_json(request)
        if invalid is not None:
            return make_json_response(from_response(invalid))

        assert request_dict is not None
        response_model = await self._article_domain.comment_service.update(UpdateCommentRequest(
            request_user_id=request['context']['user_id'],
            article_id=request.match_info['article_id'],
            comment_id=request.match_info['comment_id'],
            text=request_dict.get('text', ''),
        ))

        return make_json_response(from_response(response_model))

    async def _delete_comment(self, request: web.Request) -> web.Response:
        response_model = await self._article_domain.comment_service.delete(DeleteCommentRequest(
            request_user_id=request['context']['user_id'],
            article_id=request.match_info['article_id'],
            comment_id=request.match_info['comment_id'],
        ))

        return make_json_response(from_response(response_model))
