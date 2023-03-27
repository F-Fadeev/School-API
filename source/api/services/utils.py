from collections.abc import Generator

from source.db.database import session


def get_db() -> Generator:
    with session() as db:
        yield db
