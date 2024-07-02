from pwdlib import PasswordHash


class PasswordController:
    def __init__(self) -> None:
        self.pwd_context = PasswordHash.recommended()

    def get_password_hash(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def verify_password(self, password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(password, hashed_password)


password_controller = PasswordController()
