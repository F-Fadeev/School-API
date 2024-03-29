from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy_utils import database_exists, create_database, drop_database

from config import settings
from main import app
from source.api.auth.auth_handler import sign_jwt
from source.api.services.utils import get_db
from source.db.database import Base
from tests.upload_test_data import load_test_data

engine = create_engine(settings.get_test_db_url())


@pytest.fixture(scope='session', autouse=True)
def create_db() -> Generator:
    if not database_exists(engine.url):
        create_database(engine.url)
        Base.metadata.create_all(engine)
    else:
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)
    session = sessionmaker(bind=engine)
    load_test_data(get_session=session())
    yield
    drop_database(engine.url)


@pytest.fixture()
def db() -> Generator:
    connection = engine.connect()
    connection.begin()
    db = Session(bind=connection)
    yield db
    db.rollback()
    connection.close()


@pytest.fixture()
def get_client(db) -> Generator:
    app.dependency_overrides[get_db] = lambda: db
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope='session')
def get_token() -> str:
    return sign_jwt()['access_token']
