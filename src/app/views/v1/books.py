from fastapi import APIRouter

from src.app.controllers.books import (
    CreateBookController,
    DeleteBookController,
    ListBookController,
    RetrieveBookController,
    UpdateBookController,
)

router = APIRouter()


@router.post("/v1/livros")
def create_books():
    return CreateBookController.handle()


@router.delete("/v1/livros/{id}")
def delete_books(id: int):
    return DeleteBookController.handle(id)


@router.patch("/v1/livros/{id}")
def update_books(id: int):
    return UpdateBookController.handle(id)


@router.get("/v1/livros/{id}")
def retrieve_books(id: int):
    return RetrieveBookController.handle(id)


@router.get("/v1/livros")
def list_books():
    return ListBookController.handle()
