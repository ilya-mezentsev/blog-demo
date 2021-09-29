import json

from aiohttp import web

from .model import ResponseModel


__all__ = [
    'make_json_response',
]


def make_json_response(model: ResponseModel) -> web.Response:

    body = None
    content_type = None
    if model.body is not None:
        content_type = 'application/json'
        body = json.dumps(model.body)

    return web.Response(
        status=model.http_status,
        body=body,
        content_type=content_type,
        headers=model.headers,
    )
