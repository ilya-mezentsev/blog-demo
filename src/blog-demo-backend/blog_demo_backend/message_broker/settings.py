from dataclasses import dataclass


__all__ = [
    'MessageBrokerConfig',
]


@dataclass
class MessageBrokerConfig:
    host: str
