from http import HTTPStatus

import pytest

from src.app.controllers.utils import password_controller
from src.app.models.users import User


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


def test_change_account_success(client, session):
    hashed_password = password_controller.get_password_hash("iamcatwoman")
    cat_woman = User(
        username="selinakyle",
        password=hashed_password,
        email="selinakyle@dccomics.com",
    )
    session.add(cat_woman)
    session.commit()
    session.refresh(cat_woman)

    response = client.post(
        "/v1/token",
        data={"username": cat_woman.email, "password": "iamcatwoman"},
    )
    token = response.json()["access_token"]

    response = client.put(
        f"/v1/contas/{cat_woman.id}",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "username": "edwardnygma",
            "email": "edwardnygma@dccomics.com",
            "password": "iamriddler",
        },
    )
    response_json = response.json()

    assert response.status_code == HTTPStatus.OK
    assert response_json["username"] == "edwardnygma"
    assert response_json["email"] == "edwardnygma@dccomics.com"
    assert isinstance(response_json["id"], int)


def test_change_account_unauthorized(client, session):
    hashed_password = password_controller.get_password_hash("iambane")
    bane = User(
        username="bane",
        password=hashed_password,
        email="bane@dccomics.com",
    )
    session.add(bane)
    session.commit()
    session.refresh(bane)

    response = client.post(
        "/v1/token",
        data={"username": bane.email, "password": "iambane"},
    )
    token = response.json()["access_token"]

    response = client.put(
        "/v1/contas/1993",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "username": "edwardnygma",
            "email": "edwardnygma@dccomics.com",
            "password": "iamriddler",
        },
    )

    expected_error = {
        "detail": "Usuário não possui autorização para esse recurso",
    }

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == expected_error


def test_delete_account_success(client, session):
    hashed_password = password_controller.get_password_hash("iamscarecrow")
    scarecrow = User(
        username="scarecrow",
        password=hashed_password,
        email="scarecrow@dccomics.com",
    )
    session.add(scarecrow)
    session.commit()
    session.refresh(scarecrow)

    response = client.post(
        "/v1/token",
        data={"username": scarecrow.email, "password": "iamscarecrow"},
    )
    token = response.json()["access_token"]

    response = client.delete(
        f"/v1/contas/{scarecrow.id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"message": "Conta deletada com sucesso"}


def test_delete_account_unauthorized(client, session):
    hashed_password = password_controller.get_password_hash("iamscarecrow")
    scarecrow = User(
        username="scarecrow",
        password=hashed_password,
        email="scarecrow@dccomics.com",
    )
    session.add(scarecrow)
    session.commit()
    session.refresh(scarecrow)

    response = client.post(
        "/v1/token",
        data={"username": scarecrow.email, "password": "iamscarecrow"},
    )
    token = response.json()["access_token"]

    response = client.delete(
        "/v1/contas/1930",
        headers={"Authorization": f"Bearer {token}"},
    )

    expected_error = {
        "detail": "Usuário não possui autorização para esse recurso",
    }

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == expected_error


def test_create_and_refresh_token_success(client, session):
    hashed_password = password_controller.get_password_hash("iamharveydent")
    harveydent = User(
        username="harveydent",
        password=hashed_password,
        email="harveydent@dccomics.com",
    )
    session.add(harveydent)
    session.commit()
    session.refresh(harveydent)

    response_token = client.post(
        "/v1/token",
        data={"username": harveydent.email, "password": "iamharveydent"},
    )

    assert response_token.status_code == HTTPStatus.OK
    assert "access_token" in response_token.json()
    assert "token_type" in response_token.json()

    token = response_token.json()["access_token"]

    response_refresh_token = client.post(
        "/v1/refresh-token",
        headers={"Authorization": f"Bearer {token}"},
        data={"username": harveydent.email, "password": "iamharveydent"},
    )

    assert response_refresh_token.status_code == HTTPStatus.OK
    assert "access_token" in response_refresh_token.json()
    assert "token_type" in response_refresh_token.json()
