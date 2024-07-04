from pydantic import BaseModel, Field, field_validator


class BookRequest(BaseModel):
    title: str = Field(..., title="Título do livro")
    year: int = Field(..., title="Ano de publicação")
    novelist_id: int = Field(..., title="ID do romancista")

    @field_validator("title")
    @classmethod
    def format_title(cls, title: str) -> str:
        return " ".join(title.strip().split()).lower()


class BookQueryParams(BaseModel):
    title: str = Field(..., title="Título do livro")
    year: int = Field(..., title="Ano de publicação")
