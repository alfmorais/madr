from http import HTTPStatus

import pytest
from fastapi import HTTPException

from src.app.controllers.accounts import (
    CreateAccountControllers,
    DeleteAccountControllers,
)
from src.app.schemas.requests.accounts import UserRequest


def test_delete_accounts_success(session):
    batman = UserRequest(**{
        "username": "bruce-wayne",
        "password": "iambatman",
        "email": "bruce.wayne@wayneenterprises.com",
    })

    batman_instance = CreateAccountControllers.handle(
        user=batman,
        session=session,
    )

    response = DeleteAccountControllers.handle(
        id=batman_instance.id,
        session=session,
    )

    assert response == {"message": "Conta deletada com sucesso"}


def test_delete_accounts_not_found_user_error(session):
    with pytest.raises(HTTPException) as error:
        DeleteAccountControllers.handle(id=1984, session=session)

    assert error.typename == "HTTPException"
    assert error.value.detail == "Usuário com ID: 1984 não encontrado"
    assert error.value.status_code == HTTPStatus.NOT_FOUND
    assert issubclass(error.type, HTTPException)
