from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.app.models.books import Book
from src.app.schemas.responses.books import BookDeleted


class DeleteBookController:
    @classmethod
    def handle(cls, id: int, session: Session) -> BookDeleted:
        book = session.scalar(select(Book).where(Book.id == id))

        if book:
            session.delete(book)
            session.commit()
            return {"message": "Livro deletado no MADR"}

        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=f"Livro com ID: {id} não consta no MADR",
        )
