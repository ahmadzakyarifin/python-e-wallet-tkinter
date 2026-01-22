from backend.database.connection import get_db_connection
import hashlib

class AuthRepository:

    def _hash(self, text):
        return hashlib.sha256(text.encode()).hexdigest()

    def login(self, username, password):
        conn = get_db_connection()
        cur = conn.cursor(dictionary=True)

        cur.execute(
            "SELECT id, password FROM akun WHERE username=%s",
            (username,)
        )
        user = cur.fetchone()
        conn.close()

        if not user:
            return None

        if user["password"] == self._hash(password):
            return user["id"]

        return None

    def register(self, username, email, password, no_hp):
        conn = get_db_connection()
        cur = conn.cursor()

        try:
            cur.execute(
                "SELECT id FROM akun WHERE username=%s OR email=%s",
                (username, email)
            )
            if cur.fetchone():
                return False, "Username / Email sudah terdaftar"

            cur.execute("""
                INSERT INTO akun (username,email,password,no_telp,saldo)
                VALUES (%s,%s,%s,%s,0)
            """, (
                username,
                email,
                self._hash(password),
                no_hp
            ))

            conn.commit()
            return True, "Registrasi berhasil"

        except Exception as e:
            conn.rollback()
            return False, str(e)
        finally:
            conn.close()

    def check_email(self, email):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id FROM akun WHERE email=%s", (email,))
        res = cur.fetchone()
        conn.close()
        return res[0] if res else None

    def update_password_by_email(self, email, new_password):
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            hashed = self._hash(new_password)
            cur.execute("UPDATE akun SET password=%s WHERE email=%s", (hashed, email))
            conn.commit()
            conn.close()
            return True
        except Exception:
            return False
