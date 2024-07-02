from src.app.controllers.utils import token_controller
from src.app.models.users import User
from src.app.schemas.responses.accounts import BearerToken, TokenType


class CreateAccountTokenRefreshControllers:
    @classmethod
    def handle(cls, user: User) -> BearerToken:
        new_access_token = token_controller.create_access_token(
            data={"sub": user.email}
        )
        token = {
            "access_token": new_access_token,
            "token_type": TokenType.BEARER.value,
        }
        return token
