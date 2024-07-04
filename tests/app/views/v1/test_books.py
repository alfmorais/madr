from http import HTTPStatus

from src.app.models.books import Book


def test_create_book(
    client,
    token,
    novelist,
    session,
    user,
):
    response = client.post(
        "/v1/livros",
        headers={"Authorization": f"Bearer {token}"},
        json={"title": "New Book", "year": 2023, "novelist_id": novelist.id},
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json()["title"] == "new book"

    session.delete(user)
    session.commit()


def test_create_book_already_exist(
    client,
    token,
    novelist,
    session,
    user,
):
    response = client.post(
        "/v1/livros",
        headers={"Authorization": f"Bearer {token}"},
        json={"title": "New Book", "year": 2023, "novelist_id": novelist.id},
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json()["detail"] == "Livro com o título new book já existe"

    session.delete(user)
    session.commit()


def test_delete_book(
    client,
    token,
    session,
    user,
):
    book = Book(title="foundation", year=1951, novelist_id=1)
    session.add(book)
    session.commit()
    session.refresh(book)

    response = client.delete(
        f"/v1/livros/{book.id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json()["message"] == "Livro deletado no MADR"

    session.delete(user)
    session.commit()


def test_delete_book_not_found(client, token, session, user):
    response = client.delete(
        "/v1/livros/999",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json()["detail"] == "Livro com ID: 999 não consta no MADR"

    session.delete(user)
    session.commit()


def test_update_book(client, token, session, user):
    book = Book(title="foundation", year=1951, novelist_id=1)
    session.add(book)
    session.commit()
    session.refresh(book)

    response = client.patch(
        f"/v1/livros/{book.id}",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "title": "Updated Book",
            "year": 2024,
            "novelist_id": 1,
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json()["title"] == "updated book"

    session.delete(user)
    session.commit()


def test_update_book_not_found(client, token, session, user):
    response = client.patch(
        "/v1/livros/999",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "title": "Updated Book",
            "year": 2024,
            "novelist_id": 1,
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json()["detail"] == "Livro com o ID 999 não encontrado"

    session.delete(user)
    session.commit()


def test_retrieve_book(
    client,
    token,
    session,
    user,
):
    book = Book(title="foundation", year=1951, novelist_id=1)
    session.add(book)
    session.commit()
    session.refresh(book)

    response = client.get(
        f"/v1/livros/{book.id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json()["title"] == book.title

    session.delete(user)
    session.commit()


def test_retrieve_book_not_found(
    client,
    token,
    session,
    user,
):
    response = client.get(
        "/v1/livros/999",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json()["detail"] == "Livro com o ID 999 não encontrado"

    session.delete(user)
    session.commit()


def test_list_books(
    client,
    token,
    session,
    user,
):
    books = [
        {"title": "dune", "year": 1951, "novelist_id": 2},
        {"title": "hyperion", "year": 1951, "novelist_id": 2},
        {"title": "neuromancer", "year": 1951, "novelist_id": 2},
        {"title": "snow crash", "year": 1951, "novelist_id": 2},
    ]

    for book_data in books:
        book = Book(**book_data)
        session.add(book)
        session.commit()
        session.refresh(book)

    response = client.get(
        "/v1/livros",
        headers={"Authorization": f"Bearer {token}"},
        params={"title": "a", "year": 1951},
    )

    assert response.status_code == HTTPStatus.OK
    assert len(response.json()["books"]) > 0
    assert response.json()["books"][0]["title"] == "foundation"

    session.delete(user)
    session.commit()
