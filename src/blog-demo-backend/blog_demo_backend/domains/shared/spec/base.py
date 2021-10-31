from dataclasses import dataclass, asdict


__all__ = [
    'BaseSpec',
]


@dataclass
class BaseSpec:

    def __str__(self) -> str:
        d = dict(sorted(asdict(self).items()))
        return str(d)
