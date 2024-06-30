import json

import pytest
from pydantic import ValidationError

from src.app.schemas.requests.accounts import UserRequest


def test_accounts_user_request_success():
    payload = {
        "username": "jmn",
        "email": "joaquim@hotmail.com",
        "password": "123456789",
    }

    validated_user = UserRequest(**payload)

    assert validated_user.model_dump() == payload


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
                    "loc": ["password"],
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
                    "loc": ["email"],
                    "msg": "Field required",
                    "input": {
                        "username": "adriana_farias",
                        "password": "123456789",
                    },
                    "url": "https://errors.pydantic.dev/2.7/v/missing",
                }
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
                    "loc": ["username"],
                    "msg": "Field required",
                    "input": {
                        "email": "adriana_farias@comprehense.com.br",
                        "password": "123456789",
                    },
                    "url": "https://errors.pydantic.dev/2.7/v/missing",
                }
            ],
        ),
    ],
)
def test_accounts_user_request_validation_error(
    payload,
    expected_response,
):
    with pytest.raises(ValidationError) as error:
        UserRequest(**payload)

    assert error.typename == "ValidationError"
    assert json.loads(error.value.json()) == expected_response
    assert issubclass(error.type, ValidationError)
