from http import HTTPStatus

import pytest
from starlette.exceptions import HTTPException

from src.app.controllers.books import RetrieveBookController
from src.app.models.books import Book
from src.app.models.novelists import Novelist


def test_retrieve_book_success(session):
    novelist = Novelist(name="Isaac Asimov")
    session.add(novelist)
    session.commit()
    session.refresh(novelist)

    book = Book(title="Foundation", year=1951, novelist_id=novelist.id)
    session.add(book)
    session.commit()
    session.refresh(book)

    result = RetrieveBookController.handle(id=book.id, session=session)

    assert result.id == book.id
    assert result.title == "Foundation"
    assert result.year == book.year
    assert result.novelist_id == novelist.id


def test_retrieve_book_not_found(session):
    with pytest.raises(HTTPException) as error:
        RetrieveBookController.handle(id=999, session=session)

    assert error.value.status_code == HTTPStatus.BAD_REQUEST
    assert error.value.detail == "Livro com o ID 999 não encontrado"
