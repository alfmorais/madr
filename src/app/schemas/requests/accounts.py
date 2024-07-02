from pydantic import BaseModel, EmailStr


class UserRequest(BaseModel):
    username: str
    email: EmailStr
    password: str


class TokenData(BaseModel):
    username: str | None = None
