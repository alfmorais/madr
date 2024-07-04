from http import HTTPStatus

import pytest
from fastapi import HTTPException
from sqlalchemy import select

from src.app.controllers.books import DeleteBookController
from src.app.models.books import Book


def test_delete_book_success(session, book):
    response = DeleteBookController.handle(book.id, session)

    assert response["message"] == "Livro deletado no MADR"

    deleted_book = session.scalar(select(Book).where(Book.id == book.id))
    assert deleted_book is None


def test_delete_book_not_found(session):
    non_existent_book_id = 999

    with pytest.raises(HTTPException) as error:
        DeleteBookController.handle(non_existent_book_id, session)

    detail = f"Livro com ID: {non_existent_book_id} não consta no MADR"

    assert error.value.status_code == HTTPStatus.BAD_REQUEST
    assert error.value.detail == detail
