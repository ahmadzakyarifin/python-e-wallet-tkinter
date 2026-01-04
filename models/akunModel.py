from .databaseConnect import Database

class AkunModel:
    def __init__(self):
        self.db =  Database()

    def cekLogin(self, username, password):
        conn = self.db.get_connection()
        try:
            with conn.cursor() as cursor:
                sql = "SELECT * FROM akun WHERE username=%s AND password=%s"
                cursor.execute(sql, (username, password))
                user = cursor.fetchone() 
                return user
        finally:
            conn.close()

    def registrasiAkun(self, username, email, password, no_telepon):
        conn = self.db.get_connection()
        try:
            with conn.cursor() as cursor:
                sql = """INSERT INTO akun (username, email, password, no_telp, saldo) 
                         VALUES (%s, %s, %s, %s, 0)"""
                cursor.execute(sql, (username, email, password, no_telepon))
                conn.commit() # PENTING: Supaya data tersimpan permanen
                return True
        except Exception as e:
            print(f"Gagal Registrasi: {e}")
            return False
        finally:
            conn.close()

    def getSaldo(self, user_id):
        conn = self.db.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT saldo FROM akun WHERE id = %s", (user_id,))
                result = cursor.fetchone()
                return result['saldo'] if result else 0
        finally:
            conn.close()

    def ambilDataAkun(self, user_id):
        conn = self.db.get_connection()
        try:
            with conn.cursor() as cursor:
                sql = "SELECT * FROM akun WHERE id=%s"
                cursor.execute(sql, (user_id,))
                return cursor.fetchone()
        finally:
            conn.close()