from dataclasses import dataclass, asdict
from typing import Mapping, Any


__all__ = [
    'CreateResponse',
    'ReadResponse',
    'UpdateResponse',
    'DeleteResponse',
]


@dataclass
class _AsDictResponse:
    def to_dict(self) -> Mapping[str, Any]:
        return asdict(self)


@dataclass
class CreateResponse(_AsDictResponse):
    pass


@dataclass
class ReadResponse(_AsDictResponse):
    pass


@dataclass
class UpdateResponse(_AsDictResponse):
    pass


@dataclass
class DeleteResponse(_AsDictResponse):
    pass
