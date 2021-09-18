from dataclasses import dataclass


__all__ = [
    'Requester',
]


@dataclass
class Requester:
    role_id: str
