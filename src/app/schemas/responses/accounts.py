from enum import Enum

from pydantic import BaseModel, EmailStr


class TokenType(Enum):
    BEARER = "bearer"


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr


class UserDeleted(BaseModel):
    message: str


class BearerToken(BaseModel):
    access_token: str
    token_type: TokenType = TokenType.BEARER.value
