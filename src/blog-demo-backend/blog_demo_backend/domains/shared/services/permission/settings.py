from dataclasses import dataclass


__all__ = [
    'PermissionSettings',
]


@dataclass
class PermissionSettings:
    permission_resolver_url: str
    request_timeout: int
