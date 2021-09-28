from dataclasses import dataclass


__all__ = [
    'WebEntrypointSettings',
]


@dataclass
class WebEntrypointSettings:
    host: str
    port: int
