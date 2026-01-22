import customtkinter as ctk
from tkinter import messagebox
import random
import string

# --- IMPORT BACKEND ---
from backend.services.wallet_service import WalletService
from theme import Theme

# --- IMPORT VIEW ANDA (Pastikan nama file dan class sesuai) ---
from views.login import LoginApp
from views.home import HomeView
from views.history import HistoryView
from views.profile import ProfileFrame
from views.fiturTransfer import TransferView
from views.tarikTunai import WithdrawView
from views.topup import TopUpView
from views.fiturPulsa import PulsaView
from views.fiturTokenListrik import ListrikView, TokenResultView

class MainApp:
    def __init__(self, root, user_id, logout_callback):
        self.root = root
        self.logout_callback = logout_callback
        
        # Init Backend
        self.service = WalletService(user_id)
        
        self.W, self.H = 520, 930
        self.root.geometry(f"{self.W}x{self.H}")
        self.root.configure(bg=Theme.BG)

        # --- CONTAINER UTAMA ---
        self.container = ctk.CTkFrame(self.root, fg_color=Theme.BG)
        self.container.pack(fill="both", expand=True)

        # 1. Canvas untuk Home & History
        self.canvas = ctk.CTkCanvas(self.container, width=self.W, height=self.H, bg=Theme.BG, highlightthickness=0)
        
        # 2. Variable untuk menyimpan Frame aktif (Transfer, Profile, dll)
        self.active_frame = None

        self.show_page("home")

    def clear_screen(self):
        """Membersihkan layar sebelum ganti halaman"""
        # Sembunyikan Canvas
        self.canvas.pack_forget()
        self.canvas.delete("all")
        
        # Hancurkan Frame Aktif jika ada
        if self.active_frame:
            self.active_frame.destroy()
            self.active_frame = None

    def get_user_dict(self):
        """Ambil data terbaru dari DB dan convert ke Dict untuk UI"""
        user = self.service.get_current_user_data()
        if not user:
            messagebox.showerror("Error", "Gagal memuat data user")
            self.handle_logout()
            return {}
        return user.to_dict()

    # --- NAVIGATION LOGIC ---
    def show_page(self, page_name):
        self.clear_screen()
        user_data = self.get_user_dict()

        if page_name == "home":
            self.canvas.pack(fill="both", expand=True)
            # HomeView menggambar di canvas
            view = HomeView(self.canvas, self.W, self.H, self.show_page, user_data)
            view.draw()

        elif page_name == "history":
            self.canvas.pack(fill="both", expand=True)
            # HistoryView menggambar di canvas
            view = HistoryView(self.canvas, self.W, self.H, self.show_page, user_data["riwayat_transaksi"])
            view.draw()

        elif page_name == "profile":
            # ProfileFrame adalah CTkFrame
            self.active_frame = ProfileFrame(
                self.container, user_data, 
                navigate_callback=self.handle_profile_edit, # Callback utk edit
                logout_callback=self.handle_logout,
                back_to_home_callback=lambda: self.show_page("home")
            )
            self.active_frame.pack(fill="both", expand=True)

        # --- FITUR TRANSAKSI (Menggunakan Frame) ---
        elif page_name == "fitur_transfer":
            self.active_frame = TransferView(self.container, user_data, self.show_page, self.handle_transfer)
            self.active_frame.pack(fill="both", expand=True)

        elif page_name == "fitur_topup":
            self.active_frame = TopUpView(self.container, user_data, self.show_page, self.handle_topup)
            self.active_frame.pack(fill="both", expand=True)
            
        elif page_name == "fitur_tarik":
            self.active_frame = WithdrawView(self.container, user_data, self.show_page, self.handle_withdraw)
            self.active_frame.pack(fill="both", expand=True)

        elif page_name == "fitur_pulsa":
            self.active_frame = PulsaView(self.container, user_data, self.show_page, self.handle_ppob)
            self.active_frame.pack(fill="both", expand=True)

        elif page_name == "fitur_listrik":
            self.active_frame = ListrikView(self.container, user_data, self.show_page, self.handle_ppob)
            self.active_frame.pack(fill="both", expand=True)

    # --- CALLBACK HANDLERS (Jembatan UI -> Service) ---

    def handle_transfer(self, nomor, nominal, catatan):
        success, msg = self.service.process_transfer(nomor, nominal, catatan)
        if success:
            messagebox.showinfo("Sukses", msg)
            self.show_page("home")
        else:
            messagebox.showerror("Gagal", msg)

    def handle_topup(self, nominal, metode):
        success, msg = self.service.process_topup(nominal, metode)
        if success:
            # Simulasi kode bayar
            kode = f"VA-88{random.randint(1000,9999)}"
            messagebox.showinfo("Top Up", f"Permintaan diterima.\nKode Bayar: {kode}\n\nNote: Saldo akan masuk otomatis.")
            self.show_page("home")
        else:
            # Menampilkan Pesan Error (Limit Penuh, dll)
            messagebox.showerror("Top Up Gagal", msg)

    def handle_withdraw(self, nominal, admin, lokasi):
        # 1. Generate Code First
        code_val = "".join(random.choices(string.digits, k=6))
        
        # 2. Pass to Service to Store
        success, msg = self.service.process_withdraw(nominal, admin, lokasi, code_val)
        if success:
            return code_val
        else:
            messagebox.showerror("Gagal", f"Tarik Tunai Gagal:\n{msg}")
            return None

    def handle_ppob(self, tipe, data):
        # Tipe: "pulsa" atau "token" (dikirim dari UI)
        if tipe == "token":
            # 1. Simulasikan Generate Token (20 digit)
            token_val = "".join(random.choices(string.digits, k=20))
            data['token'] = token_val
            data['trx_id'] = f"{random.randint(100000, 999999)}"
            
            success, msg = self.service.process_ppob(tipe, data)
            if success:
                # SUKSES -> Tampilkan Halaman Receipt (TokenResultView)
                self.clear_screen() # Bersihkan ListrikView
                self.active_frame = TokenResultView(self.container, 
                                                    token_code=token_val,
                                                    amount=data['harga'],
                                                    data_transaksi=data,
                                                    back_to_home_callback=lambda: self.show_page("home"))
                self.active_frame.pack(fill="both", expand=True)
                return
            else:
                messagebox.showerror("Transaksi Gagal", msg)
                return
        
        # PPOB Lain (Pulsa)
        success, msg = self.service.process_ppob(tipe, data)
        if success:
            messagebox.showinfo("Sukses", "Transaksi Berhasil")
            self.show_page("home")
        else:
            messagebox.showerror("Transaksi Gagal", msg)

    def handle_profile_edit(self, key, title, val):
        # ProfileFrame memanggil ini jika ingin update data, tapi logic save ada di dalam ProfileFrame
        # ProfileFrame memanggil save_callback_from_main saat tombol Simpan ditekan
        pass 
        # Note: Di ProfileFrame Anda, callback save dipassing via `save_callback_from_main` 
        # di method show_edit_page. Kita perlu handle update profile:

    # Fungsi ini yang akan dipanggil tombol "Simpan" di ProfileFrame
    def handle_update_profile(self, key, new_val):
        success, msg = self.service.update_info(key, new_val)
        if success:
            messagebox.showinfo("Sukses", msg)
            # Refresh halaman profile
            if isinstance(self.active_frame, ProfileFrame):
                # Update data lokal di UI lalu refresh
                self.active_frame.user_data[key] = new_val 
                self.active_frame.refresh_ui()
        else:
            messagebox.showerror("Gagal Update", msg)

    # Override ulang show_page khusus profile agar callback edit nyambung
    def show_page(self, page_name):
        self.clear_screen()
        user_data = self.get_user_dict()
        
        if page_name == "home":
            self.canvas.pack(fill="both", expand=True)
            HomeView(self.canvas, self.W, self.H, self.show_page, user_data).draw()
        elif page_name == "history":
            self.canvas.pack(fill="both", expand=True)
            HistoryView(self.canvas, self.W, self.H, self.show_page, user_data["riwayat_transaksi"]).draw()
        elif page_name == "profile":
            self.active_frame = ProfileFrame(
                self.container, user_data,
                navigate_callback=None, # ProfileFrame handle navigasi internal
                logout_callback=self.handle_logout,
                back_to_home_callback=lambda: self.show_page("home")
            )
            # Inject custom behavior untuk edit page
            # ProfileFrame.show_edit_page memanggil save_callback
            # Kita monkey patch atau pass logic yg benar
            orig_show_edit = self.active_frame.show_edit_page
            
            def wrapped_show_edit(k, t, v):
                orig_show_edit(k, t, v, self.handle_update_profile)
                
            self.active_frame.navigate_callback = wrapped_show_edit
            self.active_frame.pack(fill="both", expand=True)
            
        elif page_name == "fitur_transfer":
            self.active_frame = TransferView(self.container, user_data, self.show_page, self.handle_transfer)
            self.active_frame.pack(fill="both", expand=True)
        elif page_name == "fitur_topup":
            self.active_frame = TopUpView(self.container, user_data, self.show_page, self.handle_topup)
            self.active_frame.pack(fill="both", expand=True)
        elif page_name == "fitur_tarik":
            self.active_frame = WithdrawView(self.container, user_data, self.show_page, self.handle_withdraw)
            self.active_frame.pack(fill="both", expand=True)
        elif page_name == "fitur_pulsa":
            self.active_frame = PulsaView(self.container, user_data, self.show_page, self.handle_ppob)
            self.active_frame.pack(fill="both", expand=True)
        elif page_name == "fitur_listrik":
            self.active_frame = ListrikView(self.container, user_data, self.show_page, self.handle_ppob)
            self.active_frame.pack(fill="both", expand=True)

    def handle_logout(self):
        if messagebox.askyesno("Keluar", "Yakin ingin keluar?"):
            self.container.destroy()
            self.logout_callback()

# --- APP CONTROLLER ---
class AppController:
    def __init__(self):
        ctk.set_appearance_mode("Light")
        self.root = ctk.CTk()
        self.root.title("E-SAKU App")
        # Ukuran disesuaikan dengan UI Anda
        self.root.geometry("520x930") 
        self.current_app = None
        
        self.show_login()

    def show_login(self):
        self.clear_root()
        # Callback login sukses menerima user_id
        self.current_app = LoginApp(self.root, on_login_success=self.show_dashboard)

    def show_dashboard(self, user_id):
        self.clear_root()
        # Masuk dashboard dengan ID user
        self.current_app = MainApp(self.root, user_id, logout_callback=self.show_login)

    def clear_root(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = AppController()
    app.run()