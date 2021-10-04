import hashlib


__all__ = [
    'create_hash',
]


def create_hash(password: str) -> str:
    return hashlib. \
        md5(f'{password}:{password}'.encode('utf-8')). \
        hexdigest()
