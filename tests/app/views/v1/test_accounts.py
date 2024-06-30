from http import HTTPStatus

import pytest


def test_create_account_success(client):
    response = client.post(
        "/v1/contas",
        json={
            "username": "jmn",
            "email": "joaquim@hotmail.com",
            "password": "123456789",
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        "id": 1,
        "username": "jmn",
        "email": "joaquim@hotmail.com",
    }


@pytest.mark.parametrize(
    ("payload", "expected_response"),
    [
        (
            {
                "username": "adriana_farias",
                "email": "adriana_farias@comprehense.com.br",
            },
            {
                "detail": [
                    {
                        "input": {
                            "email": "adriana_farias@comprehense.com.br",
                            "username": "adriana_farias",
                        },
                        "loc": ["body", "password"],
                        "msg": "Field required",
                        "type": "missing",
                    }
                ]
            },
        ),
        (
            {
                "username": "adriana_farias",
                "password": "123456789",
            },
            {
                "detail": [
                    {
                        "input": {
                            "password": "123456789",
                            "username": "adriana_farias",
                        },
                        "loc": ["body", "email"],
                        "msg": "Field required",
                        "type": "missing",
                    }
                ]
            },
        ),
        (
            {
                "email": "adriana_farias@comprehense.com.br",
                "password": "123456789",
            },
            {
                "detail": [
                    {
                        "input": {
                            "email": "adriana_farias@comprehense.com.br",
                            "password": "123456789",
                        },
                        "loc": ["body", "username"],
                        "msg": "Field required",
                        "type": "missing",
                    }
                ]
            },
        ),
    ],
)
def test_create_account_validation_error(payload, expected_response, client):
    response = client.post("/v1/contas", json=payload)

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.json() == expected_response
