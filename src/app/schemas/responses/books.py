from typing import List

from pydantic import BaseModel, Field


class BookResponse(BaseModel):
    id: int
    title: str = Field(..., title="Título do livro")
    year: int = Field(..., title="Ano de publicação")
    novelist_id: int = Field(..., title="ID do romancista")


class BookDeleted(BaseModel):
    message: str


class BookListResponse(BaseModel):
    books: List[BookResponse]
