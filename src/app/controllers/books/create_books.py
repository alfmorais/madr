from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.app.models.books import Book
from src.app.models.novelists import Novelist
from src.app.schemas.requests.books import BookRequest
from src.app.schemas.responses.books import BookResponse


class CreateBookController:
    @classmethod
    def handle(cls, book: BookRequest, session: Session) -> BookResponse:
        book_instance = session.scalar(
            select(Book).where((Book.title == book.title)),
        )

        if book_instance:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=f"Livro com o título {book.title} já existe",
            )

        novelist = session.scalar(
            select(Novelist).where((Novelist.id == book.novelist_id))
        )

        if not novelist:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=f"Romancista com o ID {book.novelist_id} não existe",
            )

        new_book = Book(
            title=book.title,
            year=book.year,
            novelist_id=novelist.id,
        )
        session.add(new_book)
        session.commit()
        session.refresh(new_book)
        return new_book
