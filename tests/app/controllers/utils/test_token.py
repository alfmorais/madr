from jwt import decode

from src.app.controllers.utils import token_controller


def test_jwt_create_success():
    token = token_controller.create_access_token(data={"test": "test"})
    decoded_token = decode(
        token,
        token_controller.secret,
        algorithms=[token_controller.algorithm],
    )

    assert decoded_token["test"] == "test"
    assert decoded_token["exp"]
