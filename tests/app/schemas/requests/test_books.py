import pytest
from pydantic import ValidationError

from src.app.schemas.requests.books import BookQueryParams, BookRequest


def test_book_request_valid():
    data = {"title": "  The Great Gatsby  ", "year": 1925, "novelist_id": 1}
    book_request = BookRequest(**data)

    assert book_request.title == "the great gatsby"


def test_book_request_invalid():
    invalid_data = {"title": None, "year": 2023, "novelist_id": 2}

    with pytest.raises(ValidationError) as error:
        BookRequest(**invalid_data)

    assert error.typename == "ValidationError"
    assert issubclass(error.type, ValidationError)


def test_book_query_params_valid():
    espected_year = 1951
    params = {"title": "The Catcher in the Rye", "year": espected_year}
    book_query_params = BookQueryParams(**params)

    assert book_query_params.title == "The Catcher in the Rye"
    assert book_query_params.year == espected_year


def test_book_query_params_invalid():
    invalid_params = {"title": "", "year": "invalid"}

    with pytest.raises(ValidationError) as error:
        BookQueryParams(**invalid_params)

    assert error.typename == "ValidationError"
    assert issubclass(error.type, ValidationError)
