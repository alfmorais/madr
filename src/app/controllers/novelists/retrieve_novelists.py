from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.app.models.novelists import Novelist
from src.app.schemas.responses.novelists import NovelistResponse


class RetrieveNovelistController:
    @classmethod
    def handle(cls, id: int, session: Session) -> NovelistResponse:
        novelist = session.scalar(select(Novelist).where((Novelist.id == id)))

        if novelist:
            return novelist

        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=f"Romancista com o ID {id} não existe",
        )
