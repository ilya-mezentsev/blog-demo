from dataclasses import dataclass


__all__ = [
    'PermissionSettings',
]


@dataclass
class PermissionSettings:
    permission_resolver_url: str
    auth_token: str
    request_timeout: int
