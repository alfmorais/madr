from http import HTTPStatus

import pytest
from fastapi import HTTPException

from src.app.controllers.novelists import (
    CreateNovelistController,
    DeleteNovelistController,
)
from src.app.schemas.requests.novelists import NovelistRequest


def test_delete_novelist_success(session):
    novelist = NovelistRequest(name="Isaac Asimov")
    novelist_database = CreateNovelistController.handle(novelist, session)

    response = DeleteNovelistController.handle(novelist_database.id, session)

    assert response == {"message": "Romancista deletada no MADR"}


def test_delete_novelist_not_found(session):
    with pytest.raises(HTTPException) as error:
        DeleteNovelistController.handle(99, session)

    error_message = "Romancista com o ID 99 não existe"

    assert error.typename == "HTTPException"
    assert error.value.detail == error_message
    assert error.value.status_code == HTTPStatus.BAD_REQUEST
    assert issubclass(error.type, HTTPException)
