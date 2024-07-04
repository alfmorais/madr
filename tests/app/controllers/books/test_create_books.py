from http import HTTPStatus

import pytest
from fastapi import HTTPException

from src.app.controllers.books import CreateBookController
from src.app.models.books import Book
from src.app.schemas.requests.books import BookRequest


def test_create_book_success(session, novelist):
    book_request = BookRequest(
        title="foundation",
        year=1951,
        novelist_id=novelist.id,
    )

    response = CreateBookController.handle(book_request, session)

    assert response.title == book_request.title
    assert response.year == book_request.year
    assert response.novelist_id == book_request.novelist_id

    session.delete(response)
    session.delete(novelist)
    session.commit()


def test_create_book_already_exists(session, novelist):
    book = Book(title="foundation", year=1951, novelist_id=novelist.id)
    session.add(book)
    session.commit()
    session.refresh(book)

    book_request = BookRequest(
        title="foundation",
        year=1951,
        novelist_id=novelist.id,
    )

    with pytest.raises(HTTPException) as error:
        CreateBookController.handle(book_request, session)

    detail = f"Livro com o título {book_request.title} já existe"

    assert error.value.status_code == HTTPStatus.BAD_REQUEST
    assert error.value.detail == detail

    session.delete(book)
    session.delete(novelist)
    session.commit()


def test_create_book_novelist_not_found(session):
    book_request = BookRequest(title="foundation", year=1951, novelist_id=999)

    with pytest.raises(HTTPException) as error:
        CreateBookController.handle(book_request, session)

    assert error.value.status_code == HTTPStatus.BAD_REQUEST
    assert (
        error.value.detail
        == f"Romancista com o ID {book_request.novelist_id} não existe"
    )
