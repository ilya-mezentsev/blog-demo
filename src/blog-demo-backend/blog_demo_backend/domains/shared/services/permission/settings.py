from dataclasses import dataclass
from typing import Sequence


__all__ = [
    'PermissionSettings',
    'LoadLevel',
]


@dataclass
class PermissionSettings:
    permission_resolver_url: str
    request_timeout: int
    load_levels: Sequence['LoadLevel']
    critical_version_id: str


@dataclass
class LoadLevel:
    version_id: str
    max_latency: int
