from aiohttp import web

from .model import ResponseModel


__all__ = [
    'server_error',
]


def server_error(description: str) -> ResponseModel:
    return ResponseModel(
        http_status=web.HTTPServerError.status_code,
        body={
            'code': 'error',
            'description': description,
        },
    )
