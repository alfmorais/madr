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
        current_user=batman_instance,
    )

    assert response == {"message": "Conta deletada com sucesso"}


def test_delete_accounts_not_found_user_error(session, user):
    with pytest.raises(HTTPException) as error:
        DeleteAccountControllers.handle(
            id=1984,
            session=session,
            current_user=user,
        )

    assert error.typename == "HTTPException"
    assert (
        error.value.detail
        == "Usuário não possui autorização para esse recurso"
    )  # noqa E501
    assert error.value.status_code == HTTPStatus.UNAUTHORIZED
    assert issubclass(error.type, HTTPException)
