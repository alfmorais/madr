from http import HTTPStatus

import pytest
from fastapi import HTTPException

from src.app.controllers.novelists import (
    CreateNovelistController,
    UpdateNovelistController,
)
from src.app.schemas.requests.novelists import NovelistRequest


def test_update_novelist_success(session):
    novelist_request = NovelistRequest(name="Isaac Asimov")
    novelist_database = CreateNovelistController.handle(
        novelist_request,
        session,
    )

    updated_novelist_request = NovelistRequest(name="Arthur C. Clarke")
    updated_novelist = UpdateNovelistController.handle(
        novelist_database.id, updated_novelist_request, session
    )

    assert updated_novelist.id == novelist_database.id
    assert updated_novelist.name == updated_novelist_request.name


def test_update_novelist_not_found(session):
    novelist_request = NovelistRequest(name="Arthur C. Clarke")

    with pytest.raises(HTTPException) as error:
        UpdateNovelistController.handle(99, novelist_request, session)

    error_message = "Romancista com o ID 99 não existe"

    assert error.typename == "HTTPException"
    assert error.value.detail == error_message
    assert error.value.status_code == HTTPStatus.BAD_REQUEST
    assert issubclass(error.type, HTTPException)
