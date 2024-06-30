from fastapi import APIRouter

from src.app.controllers.novelists import (
    CreateNovelistController,
    DeleteNovelistController,
    ListNovelistController,
    RetrieveNovelistController,
    UpdateNovelistController,
)

router = APIRouter()


@router.post("/v1/romancistas")
def create_novelists():
    return CreateNovelistController.handle()


@router.delete("/v1/romancistas/{id}")
def delete_novelists(id: int):
    return DeleteNovelistController.handle(id)


@router.patch("/v1/romancistas/{id}")
def update_novelists(id: int):
    return UpdateNovelistController.handle(id)


@router.get("/v1/romancistas/{id}")
def retrieve_novelists(id: int):
    return RetrieveNovelistController.handle(id)


@router.get("/v1/romancistas")
def list_novelists():
    return ListNovelistController.handle()
