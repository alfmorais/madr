from http import HTTPStatus

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import DecodeError, decode
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.app.models.users import User
from src.app.schemas.requests.accounts import TokenData
from src.config.database.dependency import get_db

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
OAUTH2 = OAuth2PasswordBearer(tokenUrl="/v1/token")


def credentials_exception():
    return HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )


async def current_user(
    session: Session = Depends(get_db),
    token: str = Depends(OAUTH2),
):
    try:
        payload = decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload["sub"]

        if not username:
            raise credentials_exception()

        token_data = TokenData(username=username)

    except (DecodeError, KeyError):
        raise credentials_exception()

    user = session.scalar(
        select(User).where(
            User.email == token_data.username,
        ),
    )

    if not user:
        raise credentials_exception()

    return user
