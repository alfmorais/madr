from http import HTTPStatus

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.app.controllers.books import (
    CreateBookController,
    DeleteBookController,
    ListBookController,
    RetrieveBookController,
    UpdateBookController,
)
from src.app.controllers.utils import current_user
from src.app.models.users import User
from src.app.schemas.requests.books import BookQueryParams, BookRequest
from src.app.schemas.responses.books import (
    BookDeleted,
    BookListResponse,
    BookResponse,
)
from src.config.database.dependency import get_db

router = APIRouter(tags=["Livros"])


@router.post(
    "/v1/livros",
    status_code=HTTPStatus.CREATED,
    response_model=BookResponse,
)
def create_books(
    book: BookRequest,
    session: Session = Depends(get_db),
    current_user: User = Depends(current_user),
):
    return CreateBookController.handle(book, session)


@router.delete(
    "/v1/livros/{id}",
    status_code=HTTPStatus.OK,
    response_model=BookDeleted,
)
def delete_books(
    id: int,
    session: Session = Depends(get_db),
    current_user: User = Depends(current_user),
):
    return DeleteBookController.handle(id, session)


@router.patch(
    "/v1/livros/{id}",
    status_code=HTTPStatus.OK,
    response_model=BookResponse,
)
def update_books(
    id: int,
    book: BookRequest,
    session: Session = Depends(get_db),
    current_user: User = Depends(current_user),
):
    return UpdateBookController.handle(id, book, session)


@router.get(
    "/v1/livros/{id}",
    status_code=HTTPStatus.OK,
    response_model=BookResponse,
)
def retrieve_books(
    id: int,
    session: Session = Depends(get_db),
    current_user: User = Depends(current_user),
):
    return RetrieveBookController.handle(id, session)


@router.get(
    "/v1/livros",
    status_code=HTTPStatus.OK,
    response_model=BookListResponse,
)
def list_books(
    session: Session = Depends(get_db),
    current_user: User = Depends(current_user),
    query_params: BookQueryParams = Depends(),
):
    return ListBookController.handle(session, query_params)
