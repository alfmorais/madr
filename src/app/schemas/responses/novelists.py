from typing import List

from pydantic import BaseModel


class NovelistResponse(BaseModel):
    id: int
    name: str


class NovelistDeleted(BaseModel):
    message: str


class NovelistsResponse(BaseModel):
    novelists: List[NovelistResponse]
