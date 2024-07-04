from sqlalchemy import select
from sqlalchemy.orm import Session

from src.app.models.books import Book
from src.app.schemas.requests.books import BookQueryParams
from src.app.schemas.responses.books import BookListResponse, BookResponse


class ListBookController:
    @classmethod
    def handle(
        cls, session: Session, query_params: BookQueryParams
    ) -> BookListResponse:
        title = f"%{query_params.title}%"

        books = session.scalars(
            select(Book).filter(
                Book.title.like(title),
                Book.year == query_params.year,
            )
        ).all()

        if not books:
            return {"books": []}

        novelists = [
            BookResponse(
                id=book.id,
                title=book.title,
                year=book.year,
                novelist_id=book.novelist_id,
            ).model_dump()
            for book in books
        ]

        return {"books": novelists}
