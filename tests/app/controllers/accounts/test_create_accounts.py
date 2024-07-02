from http import HTTPStatus

import pytest
from fastapi import HTTPException

from src.app.controllers.accounts import CreateAccountControllers
from src.app.schemas.requests.accounts import UserRequest


def test_create_account_success(session):
    batman = UserRequest(**{
        "username": "bruce-wayne",
        "password": "iambatman",
        "email": "bruce.wayne@wayneenterprises.com",
    })

    batman_user_database = CreateAccountControllers.handle(
        user=batman,
        session=session,
    )

    assert batman.username == batman_user_database.username
    assert batman.password != batman_user_database.password
    assert batman.email == batman_user_database.email


@pytest.mark.parametrize(
    ("error_message", "status_code", "user_payload"),
    [
        (
            "Usuário com o username bruce-wayne já existe",
            HTTPStatus.BAD_REQUEST,
            {
                "username": "bruce-wayne",
                "password": "iambatman",
                "email": "bruce.wayne@wayneenterprises.com",
            },
        ),
        (
            "Usuário com o email bruce.wayne@wayneenterprises.com já existe",
            HTTPStatus.BAD_REQUEST,
            {
                "username": "bruce-wayne2",
                "password": "iambatman",
                "email": "bruce.wayne@wayneenterprises.com",
            },
        ),
    ],
)
def test_create_account_already_exists(
    error_message,
    status_code,
    user_payload,
    session,
):
    with pytest.raises(HTTPException) as error:
        CreateAccountControllers.handle(
            user=UserRequest(**user_payload),
            session=session,
        )

    assert error.typename == "HTTPException"
    assert error.value.detail == error_message
    assert error.value.status_code == status_code
    assert issubclass(error.type, HTTPException)
