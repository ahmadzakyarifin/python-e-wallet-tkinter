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

class TransferView(ctk.CTkFrame):
    def __init__(self, master, user_data, navigate_callback, transfer_callback):
        super().__init__(master, fg_color=Theme.BG)
        
        self.user_data = user_data
        self.navigate_callback = navigate_callback
        self.transfer_callback = transfer_callback # Callback ke MainApp untuk proses transaksi

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

        title_lbl = ctk.CTkLabel(header_frame, text="Transfer Saldo", font=("Arial", 18, "bold"), text_color=Theme.WHITE)
        title_lbl.pack(side="left", padx=10)

        # Info Saldo di Header
        saldo_txt = f"Rp {self.user_data.get('saldo', 0):,}".replace(",", ".")
        saldo_lbl = ctk.CTkLabel(header_frame, text=f"Saldo: {saldo_txt}", font=("Arial", 12), text_color="#E8F5E9")
        saldo_lbl.pack(side="right", padx=20)

        # --- SCROLLABLE CONTENT ---
        self.scroll_frame = ctk.CTkScrollableFrame(self, fg_color=Theme.BG)
        self.scroll_frame.pack(fill="both", expand=True)

        # 1. Form Input
        self.create_form_section()

        # 2. Nominal Cepat
        self.create_quick_nominal()

        # 3. Riwayat Transfer (Favorit)
        self.create_history_section()

        # 4. Tombol Aksi
        btn_kirim = ctk.CTkButton(self.scroll_frame, text="KIRIM SEKARANG", font=Theme.F_BTN,
                                  fg_color=Theme.BTN_GREEN, height=50, corner_radius=10,
                                  command=self.on_submit)
        btn_kirim.pack(fill="x", padx=20, pady=30)

    def create_form_section(self):
        card = ctk.CTkFrame(self.scroll_frame, fg_color=Theme.WHITE, corner_radius=15)
        card.pack(fill="x", padx=20, pady=20)

        # Input Nomor
        ctk.CTkLabel(card, text="Nomor Tujuan / ID E-Saku", font=("Arial", 12, "bold"), text_color=Theme.TEXT).pack(anchor="w", padx=20, pady=(20,5))
        self.entry_nomor = ctk.CTkEntry(card, placeholder_text="Contoh: 0812...", height=45, border_width=0, fg_color="#F0F0F0", text_color=Theme.TEXT)
        self.entry_nomor.pack(fill="x", padx=20, pady=(0, 15))

        # Input Nominal
        ctk.CTkLabel(card, text="Nominal (Rp)", font=("Arial", 12, "bold"), text_color=Theme.TEXT).pack(anchor="w", padx=20, pady=(0,5))
        self.entry_nominal = ctk.CTkEntry(card, placeholder_text="0", height=45, border_width=0, fg_color="#F0F0F0", text_color=Theme.TEXT)
        self.entry_nominal.pack(fill="x", padx=20, pady=(0, 15))
        self.entry_nominal.bind("<KeyRelease>", self.format_rupiah)

        # Input Catatan
        ctk.CTkLabel(card, text="Catatan (Opsional)", font=("Arial", 12, "bold"), text_color=Theme.MUTED).pack(anchor="w", padx=20, pady=(0,5))
        self.entry_catatan = ctk.CTkEntry(card, placeholder_text="Bayar hutang...", height=45, border_width=0, fg_color="#F0F0F0", text_color=Theme.TEXT)
        self.entry_catatan.pack(fill="x", padx=20, pady=(0, 20))

    def create_quick_nominal(self):
        container = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
        container.pack(fill="x", padx=20, pady=(0, 20))

        amounts = [50000, 100000, 200000, 500000]
        for amt in amounts:
            txt = f"{amt//1000}k"
            btn = ctk.CTkButton(container, text=txt, width=70, height=35, 
                                fg_color=Theme.WHITE, text_color=Theme.PRIMARY, 
                                border_width=1, border_color=Theme.PRIMARY,
                                command=lambda x=amt: self.set_nominal(x))
            btn.pack(side="left", padx=(0, 10), expand=True)

    def create_history_section(self):
        ctk.CTkLabel(self.scroll_frame, text="Transfer Terakhir", font=("Arial", 14, "bold"), text_color=Theme.TEXT).pack(anchor="w", padx=20, pady=(0, 10))
        
        # Ambil data riwayat transfer dari user_data (jika ada), kalau tidak pakai dummy
        # Ini siap menerima data dari BE: self.user_data.get('kontak_favorit', [])
        recent_list = self.user_data.get("kontak_favorit", [
            {"nama": "Budi Santoso", "nomor": "08123456789"},
            {"nama": "Siti Aminah", "nomor": "08987654321"}
        ])

        for item in recent_list:
            btn = ctk.CTkButton(self.scroll_frame, text=f"{item['nama']}\n{item['nomor']}", 
                                font=("Arial", 12), anchor="w",
                                fg_color=Theme.WHITE, text_color=Theme.TEXT, 
                                hover_color="#E0E0E0", height=50,
                                command=lambda x=item['nomor']: self.set_nomor(x))
            btn.pack(fill="x", padx=20, pady=2)

    # --- LOGIC ---
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
    
    def set_nomor(self, nomor):
        self.entry_nomor.delete(0, "end")
        self.entry_nomor.insert(0, nomor)

    def on_submit(self):
        nomor = self.entry_nomor.get()
        nominal_str = self.entry_nominal.get().replace(".", "")
        catatan = self.entry_catatan.get()

        if not nomor or not nominal_str:
            messagebox.showwarning("Data Kurang", "Nomor dan Nominal wajib diisi!")
            return

        nominal = int(nominal_str)
        
        # Panggil callback di MainApp untuk proses logic backend
        self.transfer_callback(nomor, nominal, catatan)