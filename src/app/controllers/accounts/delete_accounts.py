from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.app.models.users import User
from src.app.schemas.responses.accounts import UserDeleted


class DeleteAccountControllers:
    @classmethod
    def handle(
        cls,
        id: int,
        session: Session,
        current_user: User,
    ) -> UserDeleted:
        if current_user.id != id:
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED,
                detail="Usuário não possui autorização para esse recurso",
            )

        user_query = session.scalar(select(User).where(User.id == id))
        session.delete(user_query)
        session.commit()

        return {"message": "Conta deletada com sucesso"}
