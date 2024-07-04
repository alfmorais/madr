from http import HTTPStatus


def test_create_novelist(client, token, session, user):
    response = client.post(
        "/v1/romancistas",
        headers={"Authorization": f"Bearer {token}"},
        json={"name": "Arthur C. Clarke"},
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json()["name"] == "arthur c. clarke"

    session.delete(user)
    session.commit()


def test_create_novelist_already_exist(client, token, session, user):
    client.post(
        "/v1/romancistas",
        headers={"Authorization": f"Bearer {token}"},
        json={"name": "jonas abib"},
    )

    response = client.post(
        "/v1/romancistas",
        headers={"Authorization": f"Bearer {token}"},
        json={"name": "jonas abib"},
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert (
        response.json()["detail"]
        == "Romancista com o username jonas abib já existe"
    )

    session.delete(user)
    session.commit()


def test_delete_novelist(client, novelist, token, session, user):
    response = client.delete(
        f"/v1/romancistas/{novelist.id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json()["message"] == "Romancista deletada no MADR"

    session.delete(user)
    session.commit()


def test_delete_novelist_not_found(client, token, session, user):
    response = client.delete(
        "/v1/romancistas/999",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json()["detail"] == "Romancista com o ID 999 não existe"

    session.delete(user)
    session.commit()


def test_update_novelist(client, novelist, token, session, user):
    response = client.patch(
        f"/v1/romancistas/{novelist.id}",
        headers={"Authorization": f"Bearer {token}"},
        json={"name": "H.G. Wells"},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json()["name"] == "h.g. wells"

    session.delete(user)
    session.commit()


def test_update_novelist_not_found(client, token, session, user):
    response = client.patch(
        "/v1/romancistas/999",
        headers={"Authorization": f"Bearer {token}"},
        json={"name": "H.G. Wells"},
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json()["detail"] == "Romancista com o ID 999 não existe"

    session.delete(user)
    session.commit()


def test_retrieve_novelist(client, novelist, token, session, user):
    response = client.get(
        f"/v1/romancistas/{novelist.id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json()["name"] == novelist.name

    session.delete(user)
    session.commit()


def test_retrieve_novelist_not_found(client, token, session, user):
    response = client.get(
        "/v1/romancistas/999",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json()["detail"] == "Romancista com o ID 999 não existe"

    session.delete(user)
    session.commit()


def test_list_novelists(client, novelist, token, session, user):
    response = client.get(
        "/v1/romancistas",
        headers={"Authorization": f"Bearer {token}"},
        params={"name": "Isaac"},
    )

    assert response.status_code == HTTPStatus.OK
    assert len(response.json()["novelists"]) > 0
    assert response.json()["novelists"][0]["name"] == novelist.name

    session.delete(user)
    session.commit()
