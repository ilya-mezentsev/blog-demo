from sqlalchemy import Table  # type: ignore

from .tables import blog_tables


__all__ = [
    'get_table',
]


def get_table(name: str) -> Table:

    if name in blog_tables:
        return blog_tables.tables[name]

    raise KeyError(f'Unable to find table: {name}')
