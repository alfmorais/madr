from http import HTTPStatus

import pytest
from fastapi import HTTPException

from src.app.controllers.accounts import (
    ChangeAccountControllers,
    CreateAccountControllers,
)
from src.app.schemas.requests.accounts import UserRequest


def test_change_accounts_controllers_http_exception(session, user):
    with pytest.raises(HTTPException) as error:
        ChangeAccountControllers.handle(
            id=99,
            user={},
            session=session,
            current_user=user,
        )

    assert error.typename == "HTTPException"
    assert (
        error.value.detail
        == "Usuário não possui autorização para esse recurso"
    )
    assert error.value.status_code == HTTPStatus.UNAUTHORIZED
    assert issubclass(error.type, HTTPException)


def test_chage_accounts_controllers_success(session):
    batman = UserRequest(**{
        "username": "bruce-wayne",
        "password": "iambatman",
        "email": "bruce.wayne@wayneenterprises.com",
    })
    joker = CreateAccountControllers.handle(
        user=UserRequest(**{
            "username": "arthur-fleck",
            "password": "why-so-serious?",
            "email": "arthur-fleck@gwynplaine.com",
        }),
        session=session,
    )
    joker_id = joker.id

    updated_user = ChangeAccountControllers.handle(
        id=joker_id,
        user=batman,
        session=session,
        current_user=joker,
    )

    assert updated_user.id == joker_id
    assert updated_user.username == batman.username
    assert updated_user.password != batman.password
    assert updated_user.email == batman.email
