from typing import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from testcontainers.postgres import PostgresContainer

from src.app.application import app
from src.config.database.base import Base
from src.config.database.dependency import get_db


@pytest.fixture(scope="module")
def client(session) -> Generator:
    def get_db_override():
        return session

    with TestClient(app) as app_client:
        app.dependency_overrides[get_db] = get_db_override

        yield app_client

    app.dependency_overrides.clear()


@pytest.fixture(scope="session")
def engine():
    with PostgresContainer("postgres:16", driver="psycopg") as postgres:
        _engine = create_engine(postgres.get_connection_url())

        with _engine.begin():
            yield _engine


@pytest.fixture(scope="module")
def session(engine) -> Generator:
    Base.metadata.create_all(engine)

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = SessionLocal()

    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(engine)
