from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.app.controllers.utils import password_controller
from src.app.models.users import User
from src.app.schemas.requests.accounts import UserRequest


class CreateAccountControllers:
    @classmethod
    def handle(cls, user: UserRequest, session: Session) -> User:
        user_query = session.scalar(
            select(User).where(
                (User.username == user.username) | (User.email == user.email),
            )
        )

        if user_query:
            if user_query.username == user.username:
                raise HTTPException(
                    status_code=HTTPStatus.BAD_REQUEST,
                    detail=f"Usuário com o username {user.username} já existe",
                )
            elif user_query.email == user.email:
                raise HTTPException(
                    status_code=HTTPStatus.BAD_REQUEST,
                    detail=f"Usuário com o email {user.email} já existe",
                )

        hashed_password = password_controller.get_password_hash(user.password)
        new_user = User(
            email=user.email,
            username=user.username,
            password=hashed_password,
        )
        session.add(new_user)
        session.commit()
        session.refresh(new_user)

        return new_user
