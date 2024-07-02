from http import HTTPStatus
from unittest.mock import patch

import pytest
from fastapi import HTTPException
from jwt import DecodeError

from src.app.controllers.utils import credentials_exception, current_user
from src.app.controllers.utils.current_user import ALGORITHM, SECRET_KEY


def test_credentials_exception():
    error = credentials_exception()

    assert error.status_code == HTTPStatus.UNAUTHORIZED
    assert error.detail == "Could not validate credentials"
    assert error.headers == {"WWW-Authenticate": "Bearer"}


@patch("src.app.controllers.utils.current_user.decode")
async def test_current_user_success(mock_jwt_decode, session, token, user):
    mock_jwt_decode.return_value = {"sub": user.email}
    result = await current_user(session=session, token=token)

    assert result == user
    mock_jwt_decode.assert_called_once_with(
        token,
        SECRET_KEY,
        algorithms=[ALGORITHM],
    )


@patch("src.app.controllers.utils.current_user.decode")
async def test_current_user_invalid_token(mock_jwt_decode, session):
    mock_jwt_decode.return_value = {}

    with pytest.raises(HTTPException) as error:
        await current_user(session=session, token="any-token")

    assert error.value.status_code == HTTPStatus.UNAUTHORIZED
    assert error.value.detail == "Could not validate credentials"
    mock_jwt_decode.assert_called_once_with(
        "any-token",
        SECRET_KEY,
        algorithms=[ALGORITHM],
    )


@patch("src.app.controllers.utils.current_user.decode")
async def test_current_user_user_not_found(mock_jwt_decode, session):
    mock_jwt_decode.return_value = {"sub": "joker"}

    with pytest.raises(HTTPException) as error:
        await current_user(session=session, token="any-token")

    assert error.value.status_code == HTTPStatus.UNAUTHORIZED
    assert error.value.detail == "Could not validate credentials"
    mock_jwt_decode.assert_called_once_with(
        "any-token",
        SECRET_KEY,
        algorithms=[ALGORITHM],
    )


@patch("src.app.controllers.utils.current_user.decode")
async def test_current_user_not_found_username(mock_jwt_decode, session):
    mock_jwt_decode.return_value = {"sub": None}

    with pytest.raises(HTTPException) as error:
        await current_user(session=session, token="any-token")

    assert error.value.status_code == HTTPStatus.UNAUTHORIZED
    assert error.value.detail == "Could not validate credentials"
    mock_jwt_decode.assert_called_once_with(
        "any-token",
        SECRET_KEY,
        algorithms=[ALGORITHM],
    )


@patch("src.app.controllers.utils.current_user.decode")
async def test_current_user_decode_error(mock_jwt_decode, session):
    mock_jwt_decode.side_effect = DecodeError()

    with pytest.raises(HTTPException) as error:
        await current_user(session=session, token="any-token")

    assert error.value.status_code == HTTPStatus.UNAUTHORIZED
    assert error.value.detail == "Could not validate credentials"
    mock_jwt_decode.assert_called_once_with(
        "any-token",
        SECRET_KEY,
        algorithms=[ALGORITHM],
    )
