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
from src.app.controllers.utils import current_user
from src.app.models.users import User
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
    current_user: User = Depends(current_user),
):
    return ChangeAccountControllers.handle(id, user, session, current_user)


@router.delete(
    "/v1/contas/{id}",
    status_code=status.HTTP_200_OK,
    response_model=UserDeleted,
)
def delete_accounts(
    id: int,
    session: Session = Depends(get_db),
    current_user: User = Depends(current_user),
):
    return DeleteAccountControllers.handle(id, session, current_user)


@router.post(
    "/v1/token",
    status_code=status.HTTP_200_OK,
    response_model=BearerToken,
)
def create_accounts_token(
    credentials: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: Session = Depends(get_db),
):
    return CreateAccountTokenControllers.handle(credentials, session)


@router.post(
    "/v1/refresh-token",
    status_code=status.HTTP_200_OK,
    response_model=BearerToken,
)
def create_accounts_refresh_token(user: User = Depends(current_user)):
    return CreateAccountTokenRefreshControllers.handle()
