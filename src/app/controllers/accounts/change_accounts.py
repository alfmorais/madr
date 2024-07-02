from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.app.controllers.utils import password_controller
from src.app.models.users import User
from src.app.schemas.requests.accounts import UserRequest
from src.app.schemas.responses.accounts import UserResponse


class ChangeAccountControllers:
    @classmethod
    def handle(
        cls,
        id: int,
        user: UserRequest,
        session: Session,
    ) -> UserResponse:
        user_query = session.scalar(select(User).where(User.id == id))

        if not user_query:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f"Usuário com ID: {id} não encontrado",
            )

        password = password_controller.get_password_hash(user.password)

        user_query.username = user.username
        user_query.email = user.email
        user_query.password = password
        session.commit()
        session.refresh(user_query)

        return user_query
