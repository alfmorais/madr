from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.app.models.novelists import Novelist
from src.app.schemas.requests.novelists import NovelistRequest
from src.app.schemas.responses.novelists import NovelistResponse


class CreateNovelistController:
    @classmethod
    def handle(
        cls,
        novelist: NovelistRequest,
        session: Session,
    ) -> NovelistResponse:
        novelist_query = session.scalar(
            select(Novelist).where((Novelist.name == novelist.name))
        )

        if novelist_query:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=f"Romancista com o username {novelist.name} já existe",
            )

        new_novelist = Novelist(name=novelist.name)
        session.add(new_novelist)
        session.commit()
        session.refresh(new_novelist)

        return new_novelist
