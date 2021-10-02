import datetime
import json
from typing import Any

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
        body = json.dumps(
            obj=model.body,
            default=_custom_serializer,
        )

    response = web.Response(
        status=model.http_status,
        body=body,
        content_type=content_type,
        headers=model.headers,
    )

    if model.cookies is not None:
        for key, value in model.cookies.items():
            response.set_cookie(
                name=key,
                value=value,

                # Этот хардко пока пойдет
                max_age=86400,
                httponly=True,
            )

    return response


def _custom_serializer(obj: Any) -> Any:

    if isinstance(obj, datetime.datetime):
        return obj.strftime('%d-%m-%Y, %H:%M:%S')

    raise TypeError(f'Unknown type: {type(obj)!r}')
