from http import HTTPStatus

from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.app.controllers.utils import password_controller, token_controller
from src.app.models.users import User
from src.app.schemas.responses.accounts import BearerToken, TokenType


class CreateAccountTokenControllers:
    @classmethod
    def handle(
        cls,
        credentials: OAuth2PasswordRequestForm,
        session: Session,
    ) -> BearerToken:
        error = HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Incorrect email or password",
        )
        user = session.scalar(
            select(User).where(
                User.email == credentials.username,
            )
        )

        if not user:
            raise error

        is_valid_password = password_controller.verify_password(
            credentials.password,
            user.password,
        )
        if not is_valid_password:
            raise error

        access_token = token_controller.create_access_token(
            data={"sub": user.email},
        )
        token = {
            "access_token": access_token,
            "token_type": TokenType.BEARER.value,
        }
        return token
