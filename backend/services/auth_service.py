from backend.repositories.auth_repo import AuthRepository
import backend.utils.validator as validator

class AuthService:
    def __init__(self):
        self.repo = AuthRepository()

    def login(self, username, password):
        return self.repo.login(username, password)


    def register(self, username, email, password, no_hp):
        # 1. Validasi Username (Dilonggarkan)
        if not username:
             return False, "Username tidak boleh kosong"

        # 2. Validasi Email
        if not validator.is_valid_email(email):
            return False, "Format email tidak valid."

        # 3. Validasi Telepon
        if not validator.is_valid_phone(no_hp):
            return False, "Nomor HP harus diawali 08 dan 10-13 digit."

        # 4. Validasi Kekuatan Password
        if not validator.is_valid_password(password):
            return False, "Password harus min. 8 karakter, ada huruf dan angka."

        return self.repo.register(username, email, password, no_hp)
