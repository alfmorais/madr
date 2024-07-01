from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.app.models.users import User
from src.app.schemas.responses.accounts import UserDeleted


class DeleteAccountControllers:
    @classmethod
    def handle(cls, id: int, session: Session) -> UserDeleted:
        user_query = session.scalar(select(User).where(User.id == id))

        if not user_query:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f"Usuário com ID: {id} não encontrado",
            )

        session.delete(user_query)
        session.commit()

        return {"message": "Conta deletada com sucesso"}