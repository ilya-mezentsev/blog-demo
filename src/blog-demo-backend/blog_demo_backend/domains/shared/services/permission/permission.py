import logging
from typing import (
    Mapping,
    Callable,
    Awaitable,
)

import aiohttp
from aiocache import cached  # type: ignore

from .settings import PermissionSettings
from .types import (
    IPermissionService,
    PermissionRequest,
    PermissionEffect,
)


__all__ = [
    'PermissionService',
]


def has_permission_key_builder(
        has_permission: Callable[[PermissionRequest], Awaitable[bool]],
        service: 'PermissionService',
        request: PermissionRequest,
) -> str:

    return f'{service.__class__.__name__}.{has_permission.__name__}({str(request)})'


class PermissionService(IPermissionService):
    def __init__(
            self,
            settings: PermissionSettings,
    ) -> None:

        self._settings = settings

    @cached(
        ttl=300,
        key_builder=has_permission_key_builder,
    )
    async def has_permission(self, request: PermissionRequest) -> bool:
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(
                        url=self._settings.permission_resolver_url,
                        params=self._make_params(request),
                        timeout=self._settings.request_timeout,
                ) as response:

                    response.raise_for_status()
                    response_data = await response.json()

                    return response_data.get('data', {}).get('effect') == PermissionEffect.PERMIT.value

            except Exception as e:
                logging.exception(
                    f'Unable to resolve permission for request: {request!r}. Error - {e!r}')

                """
                Выглядит очень неправильным возвращать тут False,
                т.к., например, падение сервиса ограничения доступа
                приведет к полной недоступности функционала бекенда.
                """
                return True

    @staticmethod
    def _make_params(request: PermissionRequest) -> Mapping[str, str]:
        params = {
            'roleId': request.role_id,
            'resourceId': request.resource_id,
            'operation': request.operation.value,
        }
        if request.version_id is not None:
            params['versionId'] = request.version_id

        return params
