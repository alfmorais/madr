from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.app.models.books import Book
from src.app.schemas.responses.books import BookResponse


class RetrieveBookController:
    @classmethod
    def handle(cls, id: int, session: Session) -> BookResponse:
        book = session.scalar(select(Book).where((Book.id == id)))

        if book:
            return book

        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=f"Livro com o ID {id} não encontrado",
        )
