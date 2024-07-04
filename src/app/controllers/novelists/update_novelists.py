from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.app.models.novelists import Novelist
from src.app.schemas.requests.novelists import NovelistRequest
from src.app.schemas.responses.novelists import NovelistResponse


class UpdateNovelistController:
    @classmethod
    def handle(
        cls,
        id: int,
        novelist: NovelistRequest,
        session: Session,
    ) -> NovelistResponse:
        query = session.scalar(select(Novelist).where((Novelist.id == id)))

        if query:
            query.name = novelist.name
            session.commit()
            session.refresh(query)

            return query

        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=f"Romancista com o ID {id} não existe",
        )
