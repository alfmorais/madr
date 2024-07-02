from datetime import datetime, timedelta

from jwt import encode
from zoneinfo import ZoneInfo


class TokenJwtController:
    def __init__(self, secret: str, algorithm: str, expire_time: int) -> None:
        self.secret = secret
        self.algorithm = algorithm
        self.expire_time = expire_time

    def create_access_token(self, data: dict) -> dict:
        to_encode = data.copy()
        now = datetime.now(tz=ZoneInfo("UTC"))
        expire = now + timedelta(minutes=self.expire_time)
        to_encode.update({"exp": expire})
        encoded_jwt = encode(to_encode, self.secret, algorithm=self.algorithm)
        return encoded_jwt


token_controller = TokenJwtController(
    secret="your-secret-key",
    algorithm="HS256",
    expire_time=30,
)
