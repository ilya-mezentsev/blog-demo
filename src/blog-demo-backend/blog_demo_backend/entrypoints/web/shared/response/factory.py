from typing import (
    Union,
    Optional,
    Mapping,
    Any,
)

from aiohttp import web

from blog_demo_backend.domains.user import CreateSessionResponse
from blog_demo_backend.domains.shared import (
    CreateResponse,
    ReadResponse,
    UpdateResponse,
    DeleteResponse,
    ServiceError,
    ForbiddenError,
    InvalidRequest,
    NotFound,
)

from .model import ResponseModel


__all__ = [
    'from_response',
    'session_response',
    'server_error',
    'unauthorized_error',
]


def from_response(response: Union[
    CreateResponse,
    ReadResponse,
    UpdateResponse,
    DeleteResponse,
    ServiceError,
]) -> ResponseModel:

    if isinstance(
        response,
        (
            CreateResponse,
            ReadResponse,
            UpdateResponse,
            DeleteResponse,
        )
    ):
        return _from_dict_ok(response.to_dict())

    elif isinstance(response, ServiceError):
        return _from_error(response)

    else:
        raise RuntimeError(f'Unknown response type: {type(response)!r}')


def _from_dict_ok(response_dict: Optional[Mapping[str, Any]]) -> ResponseModel:
    body: dict[str, Union[str, Mapping[str, Any]]] = {
        'code': 'ok',
    }

    if response_dict is not None:
        status_code = web.HTTPOk.status_code
        body['data'] = response_dict
    else:
        status_code = web.HTTPNoContent.status_code

    return ResponseModel(
        http_status=status_code,
        body=body,
    )


def _from_error(response: ServiceError) -> ResponseModel:
    if isinstance(response, ForbiddenError):
        status_code = web.HTTPForbidden.status_code

    elif isinstance(response, InvalidRequest):
        status_code = web.HTTPBadRequest.status_code

    elif isinstance(response, NotFound):
        status_code = web.HTTPNotFound.status_code

    else:
        raise RuntimeError(f'Unknown error response type: {type(response)!r}')

    return _make_error(
        status_code=status_code,
        description=response.description,
    )


def session_response(response: Union[
    CreateSessionResponse,
    ServiceError,
]) -> ResponseModel:

    if isinstance(response, CreateSessionResponse):
        return ResponseModel(
            http_status=web.HTTPNoContent.status_code,
            cookies={
                'BLOG_DEMO_USER_TOKEN': response.session.token,
            },
        )

    else:
        return _from_error(response)


def unauthorized_error(description: str) -> ResponseModel:
    return _make_error(
        web.HTTPUnauthorized.status_code,
        description=description,
    )


def server_error(description: str) -> ResponseModel:
    return _make_error(
        status_code=web.HTTPServerError.status_code,
        description=description,
    )


def _make_error(
        status_code: int,
        description: Optional[str] = None
) -> ResponseModel:
    return ResponseModel(
        http_status=status_code,
        body={
            'code': 'error',
            'description': description if description is not None else 'Unknown',
        },
    )
