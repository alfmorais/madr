from typing import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from testcontainers.postgres import PostgresContainer

from src.app.application import app
from src.app.controllers.utils import password_controller
from src.app.models.books import Book
from src.app.models.novelists import Novelist
from src.app.models.users import User
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


@pytest.fixture()
def user(session):
    password = "iambatman"
    user = User(
        username="Bruce Wayne",
        email="bruce-wayne@wayne-enterprises.com",
        password=password_controller.get_password_hash(password),
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    user.clean_password = "iambatman"
    return user


@pytest.fixture()
def token(client, user):
    response = client.post(
        "/v1/token",
        data={"username": user.email, "password": user.clean_password},
    )
    return response.json()["access_token"]


@pytest.fixture()
def novelist(session):
    novelist = Novelist(name="Isaac Asimov")
    session.add(novelist)
    session.commit()
    session.refresh(novelist)
    return novelist


@pytest.fixture()
def book(session, novelist):
    book = Book(title="Sample Book", year=2023, novelist_id=novelist.id)
    session.add(book)
    session.commit()
    return book
