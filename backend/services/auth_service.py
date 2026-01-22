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

    def initiate_forgot_password(self, email):
        # 1. Validasi format email
        if not validator.is_valid_email(email):
            return False, "Format email tidak valid"
        
        # 2. Cek email di DB
        user_id = self.repo.check_email(email)
        if not user_id:
            return False, "Email tidak terdaftar"

        # 3. Generate Token (Simulasi)
        import random, string
        otp = "".join(random.choices(string.digits, k=4))
        
        # Di real app, kirim email di sini. 
        # Kita return OTP agar UI bisa menampilkan popup
        return True, otp

    def reset_password(self, email, new_password):
        if not validator.is_valid_password(new_password):
            return False, "Password lemah (min 8 char, huruf+angka)"
        
        if self.repo.update_password_by_email(email, new_password):
            return True, "Password berhasil direset"
        return False, "Gagal mereset password"
