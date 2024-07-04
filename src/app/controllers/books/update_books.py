from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.app.models.books import Book
from src.app.schemas.requests.books import BookRequest
from src.app.schemas.responses.books import BookResponse


class UpdateBookController:
    @classmethod
    def handle(
        cls,
        id: int,
        book: BookRequest,
        session: Session,
    ) -> BookResponse:
        book_instance = session.scalar(select(Book).where((Book.id == id)))

        if book_instance:
            book_instance.title = book.title
            book_instance.year = book.year
            book_instance.novelist_id = book.novelist_id
            session.commit()
            session.refresh(book_instance)
            return book_instance

        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=f"Livro com o ID {id} não encontrado",
        )
