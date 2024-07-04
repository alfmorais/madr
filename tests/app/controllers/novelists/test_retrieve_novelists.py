from http import HTTPStatus

import pytest
from fastapi import HTTPException

from src.app.controllers.novelists import (
    CreateNovelistController,
    RetrieveNovelistController,
)
from src.app.schemas.requests.novelists import (
    NovelistRequest,
)


def test_retrieve_novelist_success(session):
    novelist_request = NovelistRequest(name="Isaac Asimov")
    novelist_database = CreateNovelistController.handle(
        novelist_request,
        session,
    )

    retrieved_novelist = RetrieveNovelistController.handle(
        novelist_database.id, session
    )

    assert retrieved_novelist.id == novelist_database.id
    assert retrieved_novelist.name == novelist_database.name


def test_retrieve_novelist_not_found(session):
    with pytest.raises(HTTPException) as error:
        RetrieveNovelistController.handle(99, session)

    error_message = "Romancista com o ID 99 não existe"

    assert error.typename == "HTTPException"
    assert error.value.detail == error_message
    assert error.value.status_code == HTTPStatus.BAD_REQUEST
    assert issubclass(error.type, HTTPException)
