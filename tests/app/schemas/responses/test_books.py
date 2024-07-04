import pytest
from pydantic import ValidationError

from src.app.schemas.responses.books import (
    BookDeleted,
    BookListResponse,
    BookResponse,
)


def test_book_response_model(expected_year=2023):
    data = {"id": 1, "title": "Sample Book", "year": 2023, "novelist_id": 1}
    book_response = BookResponse(**data)

    assert book_response.id == 1
    assert book_response.title == "Sample Book"
    assert book_response.year == expected_year
    assert book_response.novelist_id == 1

    with pytest.raises(ValidationError):
        BookResponse(
            id="invalid_id",
            title="Sample Book",
            year=2023,
            novelist_id=1,
        )


def test_book_deleted_model():
    data = {"message": "Book deleted successfully"}
    book_deleted = BookDeleted(**data)

    assert book_deleted.message == "Book deleted successfully"

    with pytest.raises(ValidationError) as error:
        BookDeleted(message=123)

    assert error.typename == "ValidationError"
    assert issubclass(error.type, ValidationError)


def test_book_list_response_model(expected_year=2023, quantity_books=2):
    data = {
        "books": [
            {"id": 1, "title": "Book 1", "year": 2022, "novelist_id": 1},
            {"id": 2, "title": "Book 2", "year": 2023, "novelist_id": 2},
        ]
    }
    book_list_response = BookListResponse(**data)

    assert len(book_list_response.books) == quantity_books
    assert book_list_response.books[0].title == "Book 1"
    assert book_list_response.books[1].year == expected_year

    with pytest.raises(ValidationError) as error:
        BookListResponse(books="invalid_books_data")

    assert error.typename == "ValidationError"
    assert issubclass(error.type, ValidationError)
