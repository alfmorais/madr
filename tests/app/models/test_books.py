import pytest
from sqlalchemy.exc import IntegrityError

from src.app.models.books import Book
from src.app.models.novelists import Novelist


def test_book_model_creation(session, expected_year=1925):
    novelist = Novelist(name="F. Scott Fitzgerald")
    session.add(novelist)
    session.commit()

    book = Book(title="The Great Gatsby", year=1925, novelist_id=novelist.id)
    session.add(book)
    session.commit()

    assert book.id is not None
    assert book.title == "The Great Gatsby"
    assert book.year == expected_year
    assert book.novelist_id == novelist.id
    assert book.novelist.name == "F. Scott Fitzgerald"


def test_book_model_unique_constraint(session):
    novelist = Novelist(name="Ernest Hemingway")
    session.add(novelist)
    session.commit()

    book1 = Book(
        title="For Whom the Bell Tolls",
        year=1940,
        novelist_id=novelist.id,
    )
    session.add(book1)
    session.commit()

    book2 = Book(
        title="For Whom the Bell Tolls",
        year=2023,
        novelist_id=novelist.id,
    )
    session.add(book2)

    with pytest.raises(IntegrityError) as error:
        session.commit()

    assert error.typename == "IntegrityError"
    assert issubclass(error.type, IntegrityError)

    session.rollback()
    session.close()


def test_book_model_relationship(session):
    novelist = Novelist(name="Jane Austen")
    session.add(novelist)
    session.commit()

    book = Book(
        title="Pride and Prejudice",
        year=1813,
        novelist_id=novelist.id,
    )
    session.add(book)
    session.commit()

    assert book.novelist is not None
    assert book.novelist_id == novelist.id
    assert novelist.books[0] == book

    session.close()
