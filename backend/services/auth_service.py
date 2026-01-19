from backend.repositories.auth_repo import AuthRepository

class AuthService:
    def __init__(self):
        self.repo = AuthRepository()

    def login(self, username, password):
        return self.repo.login(username, password)

    def register(self, username, email, password, no_hp):
        return self.repo.register(username, email, password, no_hp)
