from dataclasses import dataclass


__all__ = [
    'DBSettings',
]


@dataclass
class DBSettings:
    dialect: str
    driver: str
    user: str
    password: str
    host: str
    port: int
    db_name: str
    schema_name: str
    echo: bool = False
