from .databaseConnect import Database


class TransaksiModel:
    def __init__(self):
        self.db = Database()

    def topUp(self, akun_id, jumlah):
        conn = self.db.get_connection()
        try:
            with conn.cursor() as cursor:
                # 1. Update saldo di tabel akun
                cursor.execute(
                    "UPDATE akun SET saldo = saldo + %s WHERE id = %s",
                    (jumlah, akun_id),
                )
                # 2. Catat riwayat transaksi
                sql_log = """INSERT INTO transaksi (akun_id, jumlah, tipe, sumber, deskripsi) 
                             VALUES (%s, %s, 'MASUK', 'TOP_UP', 'Top Up Saldo')"""
                cursor.execute(sql_log, (akun_id, jumlah))
                conn.commit()
                return True
        except Exception as e:
            conn.rollback()
            return False
        finally:
            conn.close()

    def transferUang(self, pengirim_id, penerima_id, jumlah, deskripsi):
        conn = self.db.get_connection()
        try:
            with conn.cursor() as cursor:
                # A. Potong saldo pengirim
                cursor.execute(
                    "UPDATE akun SET saldo = saldo - %s WHERE id = %s",
                    (jumlah, pengirim_id),
                )
                # B. Tambah saldo penerima
                cursor.execute(
                    "UPDATE akun SET saldo = saldo + %s WHERE id = %s",
                    (jumlah, penerima_id),
                )
                # C. Log Transaksi Pengirim (KELUAR)
                cursor.execute(
                    """INSERT INTO transaksi (akun_id, jumlah, tipe, sumber, akun_lawan_id, deskripsi) 
                                  VALUES (%s, %s, 'KELUAR', 'TRANSFER', %s, %s)""",
                    (pengirim_id, jumlah, penerima_id, deskripsi),
                )
                # D. Log Transaksi Penerima (MASUK)
                cursor.execute(
                    """INSERT INTO transaksi (akun_id, jumlah, tipe, sumber, akun_lawan_id, deskripsi) 
                                  VALUES (%s, %s, 'MASUK', 'TRANSFER', %s, %s)""",
                    (penerima_id, jumlah, pengirim_id, deskripsi),
                )
                conn.commit()
                return True
        except Exception as e:
            conn.rollback()
            return False
        finally:
            conn.close()

    def getRiwayat(self, akun_id):
        conn = self.db.get_connection()
        try:
            with conn.cursor() as cursor:
                sql = """SELECT t.*, a.username as nama_lawan 
                         FROM transaksi t 
                         LEFT JOIN akun a ON t.akun_lawan_id = a.id 
                         WHERE t.akun_id = %s 
                         ORDER BY t.created_at DESC"""
                cursor.execute(sql, (akun_id,))
                return cursor.fetchall()
        finally:
            conn.close()
