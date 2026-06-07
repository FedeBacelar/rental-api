import bcrypt


class PasswordService:
    BCRYPT_ROUNDS = 12

    @staticmethod
    def hash_password(password: str) -> str:
        password_bytes = password.encode("utf-8")
        password_hash = bcrypt.hashpw(
            password_bytes,
            bcrypt.gensalt(rounds=PasswordService.BCRYPT_ROUNDS),
        )
        return password_hash.decode("utf-8")

    @staticmethod
    def verify_password(password: str, password_hash: str) -> bool:
        try:
            return bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8"))
        except ValueError:
            return False
