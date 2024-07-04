from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.app.controllers.novelists import (
    CreateNovelistController,
    DeleteNovelistController,
    ListNovelistController,
    RetrieveNovelistController,
    UpdateNovelistController,
)
from src.app.controllers.utils import current_user
from src.app.models.users import User
from src.app.schemas.requests.novelists import (
    NovelistListQueryParams,
    NovelistRequest,
)
from src.app.schemas.responses.novelists import (
    NovelistDeleted,
    NovelistResponse,
    NovelistsResponse,
)
from src.config.database.dependency import get_db

router = APIRouter(tags=["Romancistas"])


@router.post("/v1/romancistas", response_model=NovelistResponse)
def create_novelists(
    novelist: NovelistRequest,
    session: Session = Depends(get_db),
    current_user: User = Depends(current_user),
):
    return CreateNovelistController.handle(novelist, session)


@router.delete("/v1/romancistas/{id}", response_model=NovelistDeleted)
def delete_novelists(
    id: int,
    session: Session = Depends(get_db),
    current_user: User = Depends(current_user),
):
    return DeleteNovelistController.handle(id, session)


@router.patch("/v1/romancistas/{id}", response_model=NovelistResponse)
def update_novelists(
    id: int,
    novelist: NovelistRequest,
    session: Session = Depends(get_db),
    current_user: User = Depends(current_user),
):
    return UpdateNovelistController.handle(id, novelist, session)


@router.get("/v1/romancistas/{id}", response_model=NovelistResponse)
def retrieve_novelists(
    id: int,
    session: Session = Depends(get_db),
    current_user: User = Depends(current_user),
):
    return RetrieveNovelistController.handle(id, session)


@router.get("/v1/romancistas", response_model=NovelistsResponse)
def list_novelists(
    session: Session = Depends(get_db),
    current_user: User = Depends(current_user),
    query_params: NovelistListQueryParams = Depends(),
):
    return ListNovelistController.handle(session, query_params)
