from pydantic import BaseModel, field_validator


class NovelistRequest(BaseModel):
    name: str

    @field_validator("name")
    @classmethod
    def format_name(cls, name: str) -> str:
        return " ".join(name.strip().split()).lower()


class NovelistListQueryParams(BaseModel):
    name: str
