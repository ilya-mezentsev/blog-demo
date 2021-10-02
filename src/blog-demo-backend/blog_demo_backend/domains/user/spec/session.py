from dataclasses import dataclass


__all__ = [
    'SessionByHash',
]


@dataclass
class SessionByHash:
    hash: str
