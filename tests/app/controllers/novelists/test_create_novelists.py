from http import HTTPStatus

import pytest
from fastapi import HTTPException

from src.app.controllers.novelists import CreateNovelistController
from src.app.schemas.requests.novelists import NovelistRequest


def test_create_novelist_success(session):
    novelist = NovelistRequest(name="Isaac Asimov")
    novelist_database = CreateNovelistController.handle(novelist, session)

    assert novelist_database.name == "isaac asimov"
    assert isinstance(novelist_database.id, int)


def test_create_novelist_error(session):
    novelist = NovelistRequest(name="Isaac Asimov")

    with pytest.raises(HTTPException) as error:
        CreateNovelistController.handle(novelist, session)

    error_message = f"Romancista com o username {novelist.name} já existe"

    assert error.typename == "HTTPException"
    assert error.value.detail == error_message
    assert error.value.status_code == HTTPStatus.BAD_REQUEST
    assert issubclass(error.type, HTTPException)
