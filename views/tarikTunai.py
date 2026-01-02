import customtkinter as ctk
from tkinter import messagebox
import os
import sys

# --- Setup Import Theme ---
current_dir = os.path.dirname(os.path.abspath(__file__)) 
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

try:
    from theme import Theme
except ImportError:
    # Fallback Theme
    class Theme:
        BG = "#F5F5F5"
        WHITE = "#FFFFFF"
        PRIMARY = "#118EEA"
        TEXT = "#333333"
        MUTED = "#888888"
        BTN_GREEN = "#00C853"
        F_HEAD = ("Arial", 16, "bold")
        F_BODY = ("Arial", 12)
        F_BTN = ("Arial", 12, "bold")

class WithdrawView(ctk.CTkFrame):
    def __init__(self, master, user_data, navigate_callback, withdraw_callback):
        super().__init__(master, fg_color=Theme.BG)
        
        self.user_data = user_data
        self.navigate_callback = navigate_callback
        self.withdraw_callback = withdraw_callback # Callback ke MainApp
        self.biaya_admin = 2500

        self.create_widgets()

    def create_widgets(self):
        # --- HEADER ---
        header_frame = ctk.CTkFrame(self, fg_color=Theme.PRIMARY, height=80, corner_radius=0)
        header_frame.pack(fill="x", anchor="n")

        # Tombol Back
        btn_back = ctk.CTkButton(header_frame, text="←", font=("Arial", 24, "bold"), 
                                 fg_color=Theme.WHITE, text_color=Theme.PRIMARY,
                                 width=40, height=40, corner_radius=20,
                                 command=lambda: self.navigate_callback("home"))
        btn_back.pack(side="left", padx=20, pady=10)

        title_lbl = ctk.CTkLabel(header_frame, text="Tarik Tunai", font=("Arial", 18, "bold"), text_color=Theme.WHITE)
        title_lbl.pack(side="left", padx=10)

        # Info Saldo
        saldo_txt = f"Rp {self.user_data.get('saldo', 0):,}".replace(",", ".")
        saldo_lbl = ctk.CTkLabel(header_frame, text=f"Saldo: {saldo_txt}", font=("Arial", 12), text_color="#E8F5E9")
        saldo_lbl.pack(side="right", padx=20)

        # --- SCROLLABLE CONTENT ---
        self.scroll_frame = ctk.CTkScrollableFrame(self, fg_color=Theme.BG)
        self.scroll_frame.pack(fill="both", expand=True)

        # Info Card
        self.create_info_card()

        # Form Input
        self.create_form_section()

        # Tombol Aksi
        btn_proses = ctk.CTkButton(self.scroll_frame, text="BUAT KODE PENARIKAN", font=Theme.F_BTN,
                                  fg_color=Theme.BTN_GREEN, height=50, corner_radius=10,
                                  command=self.on_submit)
        btn_proses.pack(fill="x", padx=20, pady=30)

    def create_info_card(self):
        info_frame = ctk.CTkFrame(self.scroll_frame, fg_color="#E3F2FD", corner_radius=10, border_width=1, border_color="#90CAF9")
        info_frame.pack(fill="x", padx=20, pady=(20, 10))
        
        inner = ctk.CTkFrame(info_frame, fg_color="transparent")
        inner.pack(padx=10, pady=10)
        
        ctk.CTkLabel(inner, text="ℹ️", font=("Arial", 20)).pack(side="left", padx=(0, 10))
        ctk.CTkLabel(inner, text="Tarik tunai tanpa kartu di ATM\nBCA, BNI, BRI, Mandiri, & Indomaret", 
                     font=("Arial", 11), text_color="#1976D2", justify="left").pack(side="left")

    def create_form_section(self):
        card = ctk.CTkFrame(self.scroll_frame, fg_color=Theme.WHITE, corner_radius=15)
        card.pack(fill="x", padx=20, pady=10)

        # Input Nominal
        ctk.CTkLabel(card, text="Nominal Penarikan (Rp)", font=("Arial", 12, "bold"), text_color=Theme.TEXT).pack(anchor="w", padx=20, pady=(20,5))
        
        self.entry_nominal = ctk.CTkEntry(card, placeholder_text="0", height=45, border_width=0, fg_color="#F0F0F0", text_color=Theme.TEXT, font=("Arial", 14))
        self.entry_nominal.pack(fill="x", padx=20, pady=(0, 10))
        self.entry_nominal.bind("<KeyRelease>", self.format_rupiah)

        # Quick Amount
        quick_frame = ctk.CTkFrame(card, fg_color="transparent")
        quick_frame.pack(fill="x", padx=20, pady=(0, 20))
        amounts = [100000, 200000, 500000, 1000000]
        for i, amt in enumerate(amounts):
            txt = f"{amt//1000}k" if amt < 1000000 else "1jt"
            btn = ctk.CTkButton(quick_frame, text=txt, width=60, height=30, 
                                fg_color="#E8F5E9", text_color=Theme.BTN_GREEN, 
                                border_width=1, border_color=Theme.BTN_GREEN,
                                command=lambda x=amt: self.set_nominal(x))
            btn.pack(side="left", padx=(0, 5), expand=True, fill="x")

        # Pilihan Lokasi
        ctk.CTkLabel(card, text="Lokasi Penarikan", font=("Arial", 12, "bold"), text_color=Theme.TEXT).pack(anchor="w", padx=20, pady=(0,5))
        self.lokasi_var = ctk.StringVar(value="ATM BCA")
        self.lokasi_menu = ctk.CTkOptionMenu(card, values=["ATM BCA", "ATM BNI", "ATM BRI", "Indomaret"],
                                             variable=self.lokasi_var, height=45, fg_color="#F0F0F0", 
                                             text_color=Theme.TEXT, button_color=Theme.PRIMARY)
        self.lokasi_menu.pack(fill="x", padx=20, pady=(0, 20))

        # Info Biaya
        biaya_frame = ctk.CTkFrame(card, fg_color="#FFF3E0", corner_radius=8)
        biaya_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        inner_biaya = ctk.CTkFrame(biaya_frame, fg_color="transparent")
        inner_biaya.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(inner_biaya, text="Biaya Admin", font=("Arial", 11), text_color="#F57C00").pack(side="left")
        ctk.CTkLabel(inner_biaya, text=f"Rp {self.biaya_admin:,}".replace(",", "."), font=("Arial", 11, "bold"), text_color="#F57C00").pack(side="right")

    # --- LOGIC UI ---
    def format_rupiah(self, event):
        value = self.entry_nominal.get().replace(".", "")
        if value.isdigit():
            formatted = f"{int(value):,}".replace(",", ".")
            self.entry_nominal.delete(0, "end")
            self.entry_nominal.insert(0, formatted)

    def set_nominal(self, amount):
        formatted = f"{amount:,}".replace(",", ".")
        self.entry_nominal.delete(0, "end")
        self.entry_nominal.insert(0, formatted)

    def on_submit(self):
        nominal_str = self.entry_nominal.get().replace(".", "")
        if not nominal_str.isdigit():
            messagebox.showwarning("Error", "Masukkan nominal yang valid")
            return
            
        nominal = int(nominal_str)
        lokasi = self.lokasi_var.get()
        
        if nominal < 50000:
            messagebox.showwarning("Error", "Minimal penarikan Rp 50.000")
            return
            
        # Panggil Callback ke MainApp (Backend Simulation)
        # MainApp akan mengembalikan 'code' jika sukses, atau None jika gagal
        kode_penarikan = self.withdraw_callback(nominal, self.biaya_admin, lokasi)
        
        if kode_penarikan:
            self.show_success_dialog(kode_penarikan, nominal, lokasi)

    def show_success_dialog(self, kode, nominal, lokasi):
        """Menampilkan Popup Kode Penarikan"""
        dialog = ctk.CTkToplevel(self)
        dialog.title("Kode Penarikan")
        dialog.geometry("350x450")
        dialog.resizable(False, False)
        # Agar dialog muncul di tengah & modal
        dialog.grab_set() 
        dialog.attributes("-topmost", True)

        ctk.CTkLabel(dialog, text="✅", font=("Arial", 60)).pack(pady=(30, 10))
        ctk.CTkLabel(dialog, text="Kode Berhasil Dibuat!", font=("Arial", 16, "bold"), text_color="#333333").pack(pady=(0, 20))

        # Frame Kode
        kode_frame = ctk.CTkFrame(dialog, fg_color=Theme.BTN_GREEN, corner_radius=12)
        kode_frame.pack(fill="x", padx=30, pady=(0, 20))
        ctk.CTkLabel(kode_frame, text="KODE PENARIKAN", font=("Arial", 11), text_color="white").pack(pady=(15, 5))
        ctk.CTkLabel(kode_frame, text=kode, font=("Arial", 28, "bold"), text_color="white").pack(pady=(0, 15))

        # Detail
        detail_frame = ctk.CTkFrame(dialog, fg_color="#F8F9FA", corner_radius=12)
        detail_frame.pack(fill="x", padx=30, pady=(0, 10))
        
        rows = [("Lokasi", lokasi), ("Total Bayar", f"Rp {nominal + self.biaya_admin:,}".replace(",", "."))]
        for label, val in rows:
            row = ctk.CTkFrame(detail_frame, fg_color="transparent")
            row.pack(fill="x", padx=15, pady=5)
            ctk.CTkLabel(row, text=label, text_color="gray", font=("Arial", 11)).pack(side="left")
            ctk.CTkLabel(row, text=val, text_color="#333", font=("Arial", 11, "bold")).pack(side="right")

        ctk.CTkLabel(dialog, text="Kode berlaku 15 menit", font=("Arial", 10), text_color="gray").pack(pady=(0, 15))
        
        ctk.CTkButton(dialog, text="Selesai", font=("Arial", 12, "bold"), fg_color=Theme.PRIMARY, 
                      command=lambda: [dialog.destroy(), self.navigate_callback("home")]).pack(fill="x", padx=30, pady=10)