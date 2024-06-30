import json

import pytest
from pydantic import ValidationError

from src.app.schemas.responses.accounts import (
    BearerToken,
    TokenType,
    UserDeleted,
    UserResponse,
)


def test_accounts_token_type_success():
    assert TokenType.BEARER.value == "bearer"


def test_accounts_user_response_success():
    user = {"username": "jmn", "email": "joaquim@hotmail.com", "id": 1}

    validated_user = UserResponse(**user)

    assert validated_user.model_dump() == user


@pytest.mark.parametrize(
    ("payload", "expected_response"),
    [
        (
            {
                "username": "adriana_farias",
                "email": "adriana_farias@comprehense.com.br",
            },
            [
                {
                    "type": "missing",
                    "loc": ["id"],
                    "msg": "Field required",
                    "input": {
                        "username": "adriana_farias",
                        "email": "adriana_farias@comprehense.com.br",
                    },
                    "url": "https://errors.pydantic.dev/2.7/v/missing",
                }
            ],
        ),
        (
            {
                "username": "adriana_farias",
                "password": "123456789",
            },
            [
                {
                    "type": "missing",
                    "loc": ["id"],
                    "msg": "Field required",
                    "input": {
                        "username": "adriana_farias",
                        "password": "123456789",
                    },
                    "url": "https://errors.pydantic.dev/2.7/v/missing",
                },
                {
                    "type": "missing",
                    "loc": ["email"],
                    "msg": "Field required",
                    "input": {
                        "username": "adriana_farias",
                        "password": "123456789",
                    },
                    "url": "https://errors.pydantic.dev/2.7/v/missing",
                },
            ],
        ),
        (
            {
                "email": "adriana_farias@comprehense.com.br",
                "password": "123456789",
            },
            [
                {
                    "type": "missing",
                    "loc": ["id"],
                    "msg": "Field required",
                    "input": {
                        "email": "adriana_farias@comprehense.com.br",
                        "password": "123456789",
                    },
                    "url": "https://errors.pydantic.dev/2.7/v/missing",
                },
                {
                    "type": "missing",
                    "loc": ["username"],
                    "msg": "Field required",
                    "input": {
                        "email": "adriana_farias@comprehense.com.br",
                        "password": "123456789",
                    },
                    "url": "https://errors.pydantic.dev/2.7/v/missing",
                },
            ],
        ),
    ],
)
def test_accounts_user_response_validation_error(payload, expected_response):
    with pytest.raises(ValidationError) as error:
        UserResponse(**payload)

    assert error.typename == "ValidationError"
    assert json.loads(error.value.json()) == expected_response
    assert issubclass(error.type, ValidationError)


def test_accounts_user_deleted_success():
    message = {"message": "I'm tea pot"}
    validated_message = UserDeleted(**message)

    assert validated_message.model_dump() == message


def test_accounts_user_deleted_validation_error():
    expected_response = [
        {
            "type": "missing",
            "loc": ["message"],
            "msg": "Field required",
            "input": {},
            "url": "https://errors.pydantic.dev/2.7/v/missing",
        }
    ]

    with pytest.raises(ValidationError) as error:
        UserDeleted(**{})

    assert error.typename == "ValidationError"
    assert json.loads(error.value.json()) == expected_response
    assert issubclass(error.type, ValidationError)


def test_accounts_bearer_token_success():
    access_token = {"access_token": "some-aleatory-token"}

    validated_access_token = BearerToken(**access_token)

    assert validated_access_token.access_token == access_token["access_token"]
    assert validated_access_token.token_type == "bearer"


def test_accounts_bearer_token_validation_error():
    expected_response = [
        {
            "type": "missing",
            "loc": ["access_token"],
            "msg": "Field required",
            "input": {},
            "url": "https://errors.pydantic.dev/2.7/v/missing",
        }
    ]

    with pytest.raises(ValidationError) as error:
        BearerToken(**{})

    assert error.typename == "ValidationError"
    assert json.loads(error.value.json()) == expected_response
    assert issubclass(error.type, ValidationError)
