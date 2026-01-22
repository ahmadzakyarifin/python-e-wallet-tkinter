from backend.repositories.wallet_repo import WalletRepository

class WalletService:
    def __init__(self, user_id):
        self.user_id = user_id
        self.repo = WalletRepository()

    def get_current_user_data(self):
        return self.repo.get_user_by_id(self.user_id)

    def process_transfer(self, nomor, nominal, catatan):
        import random, string
        ref = "".join(random.choices(string.digits, k=16))
        
        # Deskripsi untuk Pengirim
        desc_sender = f"Transfer ke {nomor}"
        if catatan:
            desc_sender += f" ({catatan})"
        desc_sender += f" (Ref: {ref})" # Add Ref
            
        # Deskripsi untuk Penerima
        desc_receiver = "Kiriman Saldo Masuk"
        if catatan:
            desc_receiver += f" ({catatan})"
        desc_receiver += f" (Ref: {ref})" # Add Ref

        # Gunakan metode transfer_balance yang baru
        return self.repo.transfer_balance(
            self.user_id, nomor, nominal, desc_sender, desc_receiver
        )

    def process_topup(self, nominal, metode):
        import random, string
        ref = "".join(random.choices(string.digits, k=16))
        return self.repo.create_transaction(
            self.user_id, nominal, "MASUK", "TOP_UP", f"Top Up via {metode} (Ref: {ref})"
        )

    def process_withdraw(self, nominal, admin, lokasi, withdraw_code):
        total = nominal + admin
        desc = f"Tarik tunai {lokasi} (Kode: {withdraw_code})"
        return self.repo.create_transaction(
            self.user_id, total, "KELUAR", "TARIK_TUNAI", desc
        )

    def process_ppob(self, tipe, data):
        if tipe == "pulsa":
            import random, string
            sn = "".join(random.choices(string.digits, k=16))
            desc = f"Pulsa {data['operator']} {data['nomor']} (SN: {sn})"
            sumber = "PULSA"
        else:
            desc = f"Token Listrik {data['meter']}"
            if 'token' in data:
                # Format to 4-4-4-4-4 (Space separated)
                raw = data['token']
                fmt_token = f"{raw[:4]} {raw[4:8]} {raw[8:12]} {raw[12:16]} {raw[16:]}"
                desc += f" (Token: {fmt_token})"
            sumber = "LISTRIK"

        return self.repo.create_transaction(
            self.user_id, data["harga"], "KELUAR", sumber, desc
        )

    def update_info(self, key, value):
        import backend.utils.validator as validator
        
        # Logika Validasi
        if key == "email":
            if not validator.is_valid_email(value):
                return False, "Format email tidak valid"
        elif key == "no_hp":
            if not validator.is_valid_phone(value):
                return False, "Nomor HP tidak valid (08...)"
        elif key == "pin": # PIN acts as Password
            if not validator.is_valid_password(value):
                return False, "Password lemah (min 8 char, huruf+angka)"
        
        # Eksekusi Pembaruan
        final_value = value
        if key == "pin":
            import hashlib
            final_value = hashlib.sha256(value.encode()).hexdigest()

        if self.repo.update_profile(self.user_id, key, final_value):
            return True, "Update berhasil"
        return False, "Gagal update database"
