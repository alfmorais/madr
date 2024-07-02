from src.app.controllers.accounts import CreateAccountTokenRefreshControllers


def test_create_account_token_refresh_success(user):
    new_token = CreateAccountTokenRefreshControllers.handle(user)

    assert "access_token" in new_token
    assert "token_type" in new_token
