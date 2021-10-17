from dataclasses import dataclass


__all__ = [
    'WebEntrypointSettings',
    'BasicAuthSettings',
]


@dataclass
class WebEntrypointSettings:
    host: str
    port: int

    basic_auth: 'BasicAuthSettings'


@dataclass
class BasicAuthSettings:
    username: str
    password: str
