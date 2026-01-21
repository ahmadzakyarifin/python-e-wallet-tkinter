from backend.repositories.wallet_repo import WalletRepository

class WalletService:
    def __init__(self, user_id):
        self.user_id = user_id
        self.repo = WalletRepository()

    def get_current_user_data(self):
        return self.repo.get_user_by_id(self.user_id)

    def process_transfer(self, nomor, nominal, catatan):
        # Deskripsi untuk Pengirim
        desc_sender = f"Transfer ke {nomor}"
        if catatan:
            desc_sender += f" ({catatan})"
            
        # Deskripsi untuk Penerima
        desc_receiver = "Kiriman Saldo Masuk"
        if catatan:
            desc_receiver += f" ({catatan})"

        # Gunakan metode transfer_balance yang baru
        return self.repo.transfer_balance(
            self.user_id, nomor, nominal, desc_sender, desc_receiver
        )

    def process_topup(self, nominal, metode):
        return self.repo.create_transaction(
            self.user_id, nominal, "MASUK", "TOP_UP", f"Top Up via {metode}"
        )

    def process_withdraw(self, nominal, admin, lokasi):
        total = nominal + admin
        return self.repo.create_transaction(
            self.user_id, total, "KELUAR", "TARIK_TUNAI", f"Tarik tunai {lokasi}"
        )

    def process_ppob(self, tipe, data):
        if tipe == "pulsa":
            desc = f"Pulsa {data['operator']} {data['nomor']}"
            sumber = "PULSA"
        else:
            desc = f"Token Listrik {data['meter']}"
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
        if self.repo.update_profile(self.user_id, key, value):
            return True, "Update berhasil"
        return False, "Gagal update database"
