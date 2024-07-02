from http import HTTPStatus

import pytest
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from src.app.controllers.accounts.create_accounts_token import (
    CreateAccountTokenControllers,
)


def test_create_account_token_success(user, session):
    credentials = OAuth2PasswordRequestForm(
        username=user.email,
        password=user.clean_password,
    )
    token = CreateAccountTokenControllers.handle(credentials, session)

    assert "access_token" in token
    assert "token_type" in token


def test_create_account_token_validation_error_user_not_found(session):
    credentials = OAuth2PasswordRequestForm(
        username="arthurfleck",
        password="iamjoker",
    )

    with pytest.raises(HTTPException) as error:
        CreateAccountTokenControllers.handle(credentials, session)

    assert error.typename == "HTTPException"
    assert error.value.detail == "Incorrect email or password"
    assert error.value.status_code == HTTPStatus.BAD_REQUEST
    assert issubclass(error.type, HTTPException)


def test_create_account_token_validation_error_password_check(session):
    credentials = OAuth2PasswordRequestForm(
        username="bruce-wayne@wayne-enterprises.com",
        password="iamjoker",
    )

    with pytest.raises(HTTPException) as error:
        CreateAccountTokenControllers.handle(credentials, session)

    assert error.typename == "HTTPException"
    assert error.value.detail == "Incorrect email or password"
    assert error.value.status_code == HTTPStatus.BAD_REQUEST
    assert issubclass(error.type, HTTPException)
