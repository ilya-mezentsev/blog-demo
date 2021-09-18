import logging

import aiohttp

from .settings import PermissionSettings
from .types import (
    IPermissionService,
    PermissionRequest,
    PermissionEffect,
)


__all__ = [
    'ServiceService',
]


class ServiceService(IPermissionService):
    def __init__(
            self,
            settings: PermissionSettings,
    ) -> None:

        self._settings = settings

    async def has_permission(self, request: 'PermissionRequest') -> bool:
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(
                        url=self._settings.permission_resolver_url,
                        headers={
                            'X-RM-Auth-Token': self._settings.auth_token,
                        },
                        timeout=self._settings.request_timeout,
                ) as response:

                    response.raise_for_status()
                    response_data = await response.json()

                    return response_data.get('data', {}).get('effect') == PermissionEffect.PERMIT

            except Exception as e:
                logging.exception(
                    f'Unable to resolve permission for request: {request!r}. Error - {e!r}')

                """
                Выглядит очень неправильным возвращать тут False,
                т.к., например, падение сервиса ограничения доступа
                приведет к полной недоступности функционала бекенда.
                """
                return True
