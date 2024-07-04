from sqlalchemy import select
from sqlalchemy.orm import Session

from src.app.models.novelists import Novelist
from src.app.schemas.requests.novelists import NovelistListQueryParams
from src.app.schemas.responses.novelists import (
    NovelistResponse,
    NovelistsResponse,
)


class ListNovelistController:
    @classmethod
    def handle(
        cls,
        session: Session,
        query_params: NovelistListQueryParams,
    ) -> NovelistsResponse:
        name_pattern = f"%{query_params.name}%"
        novelists_database = session.scalars(
            select(Novelist).filter(Novelist.name.like(name_pattern))
        ).all()

        if not novelists_database:
            return {"novelists": []}

        novelists = [
            NovelistResponse(id=novelist.id, name=novelist.name).model_dump()
            for novelist in novelists_database
        ]

        return {"novelists": novelists}
