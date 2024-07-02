from src.app.controllers.utils import password_controller


def test_password_controller_success():
    password = "iambatman"
    hashed_password = password_controller.get_password_hash(password)

    assert password != hashed_password
    assert password_controller.verify_password(password, hashed_password)
