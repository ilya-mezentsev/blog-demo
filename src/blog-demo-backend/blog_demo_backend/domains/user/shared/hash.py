import hashlib


__all__ = [
    'create_hash',
]


def create_hash(nickname: str, password: str) -> str:
    return hashlib. \
        md5(f'{nickname}:{password}'.encode('utf-8')). \
        hexdigest()
