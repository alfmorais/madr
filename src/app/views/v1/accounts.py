from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from src.app.controllers.accounts import (
    ChangeAccountControllers,
    CreateAccountControllers,
    CreateAccountTokenControllers,
    CreateAccountTokenRefreshControllers,
    DeleteAccountControllers,
)
from src.app.schemas.requests.accounts import UserRequest
from src.app.schemas.responses.accounts import (
    BearerToken,
    UserDeleted,
    UserResponse,
)
from src.config.database.dependency import get_db

router = APIRouter(tags=["Contas"])


@router.post(
    "/v1/contas",
    status_code=status.HTTP_201_CREATED,
    response_model=UserResponse,
)
def create_accounts(
    user: UserRequest,
    session: Session = Depends(get_db),
):
    return CreateAccountControllers.handle(user, session)


@router.put(
    "/v1/contas/{id}",
    status_code=status.HTTP_200_OK,
    response_model=UserResponse,
)
def change_accounts(
    id: int,
    user: UserRequest,
    session: Session = Depends(get_db),
):
    return ChangeAccountControllers.handle()


@router.delete(
    "/v1/contas/{id}",
    status_code=status.HTTP_200_OK,
    response_model=UserDeleted,
)
def delete_accounts(
    id: int,
    session: Session = Depends(get_db),
):
    return DeleteAccountControllers.handle(id, session)


@router.post(
    "/v1/token",
    status_code=status.HTTP_200_OK,
    response_model=BearerToken,
)
def create_accounts_token(
    credentials: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: Session = Depends(get_db),
):
    return CreateAccountTokenControllers.handle()


@router.post(
    "/v1/refresh-token",
    status_code=status.HTTP_200_OK,
    response_model=BearerToken,
)
def create_accounts_refresh_token(
    session: Session = Depends(get_db),
):
    return CreateAccountTokenRefreshControllers.handle()
