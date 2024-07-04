from http import HTTPStatus

import pytest
from starlette.exceptions import HTTPException

from src.app.controllers.books.update_books import UpdateBookController
from src.app.models.books import Book
from src.app.models.novelists import Novelist
from src.app.schemas.requests.books import BookRequest


def test_update_book_success(session):
    novelist = Novelist(name="Isaac Asimov")
    session.add(novelist)
    session.commit()
    session.refresh(novelist)

    book = Book(title="Foundation", year=1951, novelist_id=novelist.id)
    session.add(book)
    session.commit()
    session.refresh(book)

    updated_book_data = BookRequest(
        title="Updated Foundation", year=1952, novelist_id=novelist.id
    )

    result = UpdateBookController.handle(
        id=book.id, book=updated_book_data, session=session
    )
    assert result.id == book.id
    assert result.title == book.title
    assert result.year == book.year
    assert result.novelist_id == novelist.id


def test_update_book_not_found(session):
    updated_book_data = BookRequest(
        title="Non-Existent Book",
        year=1950,
        novelist_id=1,
    )

    with pytest.raises(HTTPException) as error:
        UpdateBookController.handle(
            id=999,
            book=updated_book_data,
            session=session,
        )

    assert error.value.status_code == HTTPStatus.BAD_REQUEST
    assert error.value.detail == "Livro com o ID 999 não encontrado"
