from aiohttp import web

from blog_demo_backend.domains import ArticleDomain


__all__ = [
    'ArticleEntrypoint',
]


class ArticleEntrypoint:

    def __init__(
            self,
            article_domain: ArticleDomain
    ) -> None:

        self._article_domain = article_domain

    def make_entrypoint(self) -> web.Application:
        app = web.Application()

        app.add_routes([
            web.post(r'', self._create_article),
            web.get(r'', self._read_articles),
            web.get(r'/{article_id}', self._read_article),
            web.patch(r'', self._update_article),
            web.delete(r'/{article_id}', self._delete_article),

            web.post(r'/{article_id}/comments', self._create_comment),
            web.get(r'/{article_id}/comments', self._read_comments),
            web.patch(r'/{article_id}/comments', self._update_comment),
            web.delete(
                r'/{article_id}/comments/{comment_id}',
                self._delete_comment,
            ),
        ])

        return app

    async def _create_article(self, request: web.Request) -> web.Response:
        raise NotImplementedError()

    async def _read_articles(self, request: web.Request) -> web.Response:
        raise NotImplementedError()

    async def _read_article(self, request: web.Request) -> web.Response:
        raise NotImplementedError()

    async def _update_article(self, request: web.Request) -> web.Response:
        raise NotImplementedError()

    async def _delete_article(self, request: web.Request) -> web.Response:
        raise NotImplementedError()

    async def _create_comment(self, request: web.Request) -> web.Response:
        raise NotImplementedError()

    async def _read_comments(self, request: web.Request) -> web.Response:
        raise NotImplementedError()

    async def _update_comment(self, request: web.Request) -> web.Response:
        raise NotImplementedError()

    async def _delete_comment(self, request: web.Request) -> web.Response:
        raise NotImplementedError()
