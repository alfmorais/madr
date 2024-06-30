from typing import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

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


@pytest.fixture(scope="module")
def session():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    Base.metadata.drop_all(engine)
