from backend.database.connection import get_db_connection
from backend.models.entity import User, Transaction
from datetime import datetime

class WalletRepository:

    def get_user_by_id(self, user_id):
        conn = get_db_connection()
        cur = conn.cursor(dictionary=True)

        # PENGGUNA
        cur.execute("SELECT * FROM akun WHERE id=%s", (user_id,))
        u = cur.fetchone()
        if not u:
            conn.close()
            return None

        # TRANSAKSI
        cur.execute("""
            SELECT id, jumlah, tipe, sumber, deskripsi, created_at
            FROM transaksi
            WHERE akun_id=%s
            ORDER BY created_at DESC
            LIMIT 10
        """, (user_id,))
        rows = cur.fetchall()

        riwayat = [
            Transaction(
                id=r["id"],
                amount=float(r["jumlah"]),
                type=r["tipe"],
                source=r["sumber"],
                description=r["deskripsi"],
                date=r["created_at"].strftime("%d %b %Y, %H:%M") if r["created_at"] else ""
            ) for r in rows
        ]

        # STATISTIK BULAN INI
        now = datetime.now()
        cur.execute("""
            SELECT
            SUM(IF(tipe='MASUK',jumlah,0)) AS masuk,
            SUM(IF(tipe='KELUAR',jumlah,0)) AS keluar
            FROM transaksi
            WHERE akun_id=%s AND MONTH(created_at)=%s AND YEAR(created_at)=%s
        """, (user_id, now.month, now.year))
        stat = cur.fetchone()

        conn.close()

        return User(
            id=u["id"],
            username=u["username"],
            email=u["email"],
            no_telp=u["no_telp"],
            saldo=float(u["saldo"]),
            target_pemasukan=float(u.get("target_pemasukan", 10_000_000)),
            limit_pengeluaran=float(u.get("limit_pengeluaran", 5_000_000)),
            pemasukan=float(stat["masuk"] or 0),
            pengeluaran=float(stat["keluar"] or 0),
            level="Gold" if (stat["masuk"] or 0) > 1_000_000 else "Silver",
            riwayat_transaksi=riwayat
        )

    # ================= TRANSAKSI =================

    def transfer_balance(self, sender_id, dest_phone, amount, desc_sender, desc_receiver):
        conn = get_db_connection()
        cur = conn.cursor()

        try:
            # 1. Cek Penerima
            cur.execute("SELECT id, username FROM akun WHERE no_telp=%s", (dest_phone,))
            receiver = cur.fetchone()
            if not receiver:
                print("Receiver not found")
                return False, "Nomor tujuan tidak ditemukan"

            receiver_id = receiver[0]
            if receiver_id == sender_id:
                print("Cannot transfer to self")
                return False, "Tidak bisa transfer ke diri sendiri"

            # 2. Key & Cek Saldo Pengirim
            cur.execute("SELECT saldo FROM akun WHERE id=%s FOR UPDATE", (sender_id,))
            sender_saldo = float(cur.fetchone()[0])

            if sender_saldo < amount:
                conn.rollback()
                return False, "Saldo tidak mencukupi"

            # 3. Eksekusi Transfer
            # A. Kurangi Pengirim
            # Modifikasi Deskripsi Pengirim: Tambahkan Nama Penerima agar muncul di Histori
            # Format: "Transfer ke 08xx (Nama) (Catatan...)"
            final_desc_sender = desc_sender.replace(f"Transfer ke {dest_phone}", f"Transfer ke {dest_phone} ({receiver[1]})")

            cur.execute("UPDATE akun SET saldo=saldo-%s WHERE id=%s", (amount, sender_id))
            cur.execute("""
                INSERT INTO transaksi (akun_id, jumlah, tipe, sumber, deskripsi)
                VALUES (%s, %s, 'KELUAR', 'TRANSFER', %s)
            """, (sender_id, amount, final_desc_sender))

            # B. Tambah Penerima
            cur.execute("UPDATE akun SET saldo=saldo+%s WHERE id=%s", (amount, receiver_id))
            cur.execute("""
                INSERT INTO transaksi (akun_id, jumlah, tipe, sumber, deskripsi)
                VALUES (%s, %s, 'MASUK', 'TRANSFER', %s)
            """, (receiver_id, amount, desc_receiver))

            conn.commit()
            return True, "Transfer Berhasil"

        except Exception as e:
            conn.rollback()
            print("DB ERROR (Transfer):", e)
            return False, "Terjadi kesalahan sistem"
        finally:
            conn.close()

    def create_transaction(self, user_id, amount, tipe, sumber, desc):
        conn = get_db_connection()
        cur = conn.cursor()

        try:
            # kunci saldo (lock)
            cur.execute("SELECT saldo FROM akun WHERE id=%s FOR UPDATE", (user_id,))
            res = cur.fetchone()
            if not res:
                return False
            saldo = res[0]

            if tipe == "KELUAR" and saldo < amount:
                conn.rollback()
                return False

            # masukkan transaksi
            cur.execute("""
                INSERT INTO transaksi (akun_id,jumlah,tipe,sumber,deskripsi)
                VALUES (%s,%s,%s,%s,%s)
            """, (user_id, amount, tipe, sumber, desc))

            # perbarui saldo
            op = "+" if tipe == "MASUK" else "-"
            cur.execute(f"""
                UPDATE akun SET saldo = saldo {op} %s WHERE id=%s
            """, (amount, user_id))

            conn.commit()
            return True

        except Exception as e:
            conn.rollback()
            print("DB ERROR:", e)
            return False
        finally:
            conn.close()

    def update_profile(self, user_id, key, value):
        mapping = {
            "nama": "username",
            "email": "email",
            "no_hp": "no_telp",
            "pin": "password"
        }
        col = mapping.get(key)
        if not col:
            return False

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(f"UPDATE akun SET {col}=%s WHERE id=%s", (value, user_id))
        conn.commit()
        conn.close()
        return True
