import customtkinter as ctk
from tkinter import messagebox
import os
import sys

# --- Pengaturan Impor Tema ---
current_dir = os.path.dirname(os.path.abspath(__file__)) 
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

try:
    from theme import Theme
except ImportError:
    class Theme:
        BG = "#F5F5F5"
        WHITE = "#FFFFFF"
        PRIMARY = "#05B048"
        TEXT = "#333333"
        MUTED = "#888888"
        BTN_GREEN = "#05B048"
        BTN_HOVER = "#008e36"
        F_HEAD = ("Arial", 16, "bold")
        F_BODY = ("Arial", 12)
        F_BTN = ("Arial", 12, "bold")

class ListrikView(ctk.CTkFrame):
    def __init__(self, master, user_data, navigate_callback, transaction_callback):
        super().__init__(master, fg_color=Theme.BG)
        self.user_data = user_data
        self.navigate_callback = navigate_callback
        self.transaction_callback = transaction_callback
        self.selected_package = None
        self.pkg_buttons = []
        self.create_widgets()

    def create_widgets(self):
        # 1. HEADER STANDAR
        header = ctk.CTkFrame(self, fg_color=Theme.PRIMARY, height=80, corner_radius=0)
        header.pack(fill="x", anchor="n")
        
        ctk.CTkButton(header, text="←", font=("Arial", 24, "bold"), fg_color=Theme.WHITE, text_color=Theme.PRIMARY,
                      width=40, height=40, corner_radius=20, cursor="hand2", hover_color=Theme.BTN_HOVER_LIGHT,
                      command=lambda: self.navigate_callback("home")).pack(side="left", padx=20, pady=10)

        ctk.CTkLabel(header, text="Token Listrik", font=("Arial", 18, "bold"), text_color=Theme.WHITE).pack(side="left", padx=10)
        
        saldo = f"Rp {self.user_data.get('saldo', 0):,}".replace(",", ".")
        ctk.CTkLabel(header, text=f"Saldo: {saldo}", font=("Arial", 12), text_color="#E8F5E9").pack(side="right", padx=20)

        # 2. KONTEN SCROLL
        self.scroll = ctk.CTkScrollableFrame(self, fg_color=Theme.BG)
        self.scroll.pack(fill="both", expand=True)

        # 3. KARTU INPUT
        card = ctk.CTkFrame(self.scroll, fg_color=Theme.WHITE, corner_radius=15)
        card.pack(fill="x", padx=20, pady=20)

        # Input ID Pelanggan
        ctk.CTkLabel(card, text="ID Pelanggan / No. Meter", font=("Arial", 12, "bold"), text_color=Theme.TEXT).pack(anchor="w", padx=20, pady=(20, 5))
        self.entry_meter = ctk.CTkEntry(card, placeholder_text="Masukkan Nomor Meter", height=50, border_width=0, 
                                        fg_color="#F0F0F0", text_color=Theme.TEXT, font=("Arial", 16, "bold"))
        self.entry_meter.pack(fill="x", padx=20, pady=(0, 15))

        # Paket
        ctk.CTkLabel(card, text="Pilih Nominal Token", font=("Arial", 12, "bold"), text_color=Theme.TEXT).pack(anchor="w", padx=20, pady=(10, 5))
        
        packages = [
            {"nominal": 20000, "harga": 22500},
            {"nominal": 50000, "harga": 52500},
            {"nominal": 100000, "harga": 102500},
            {"nominal": 200000, "harga": 202500},
            {"nominal": 500000, "harga": 502500}
        ]
        
        for pkg in packages:
            self.create_pkg_item(card, pkg)

        # 4. AKSI TOMBOL
        ctk.CTkButton(self.scroll, text="BELI TOKEN", font=Theme.F_BTN,
                      fg_color=Theme.PRIMARY, height=50, corner_radius=10, 
                      cursor="hand2", hover_color=Theme.BTN_HOVER_DARK,
                      command=self.on_submit).pack(fill="x", padx=20, pady=30)

    def create_pkg_item(self, parent, pkg):
        frame = ctk.CTkFrame(parent, fg_color="white", border_width=1, border_color="#E0E0E0", corner_radius=10)
        frame.pack(fill="x", padx=20, pady=5)
        frame.configure(cursor="hand2")
        
        ctk.CTkLabel(frame, text=f"Token {pkg['nominal']:,}".replace(",", "."), 
                     font=("Arial", 14, "bold")).pack(side="left", padx=15, pady=15)
        
        ctk.CTkLabel(frame, text=f"Rp {pkg['harga']:,}".replace(",", "."), 
                     font=("Arial", 14, "bold"), text_color=Theme.PRIMARY).pack(side="right", padx=15)
        
        def on_click(e):
            self.selected_package = pkg
            for btn in self.pkg_buttons: 
                btn.configure(border_color="#E0E0E0", fg_color=Theme.WHITE)
            frame.configure(border_color=Theme.PRIMARY, fg_color="#E8F5E9")
            
        # Hover
        def on_enter(e):
            if self.selected_package != pkg:
                frame.configure(border_color=Theme.PRIMARY)
        def on_leave(e):
            if self.selected_package != pkg:
                frame.configure(border_color="#E0E0E0")

        frame.bind("<Button-1>", on_click)
        frame.bind("<Enter>", on_enter)
        frame.bind("<Leave>", on_leave)

        for c in frame.winfo_children(): 
            c.bind("<Button-1>", on_click)
            c.bind("<Enter>", on_enter)
            c.bind("<Leave>", on_leave)
        
        self.pkg_buttons.append(frame)

    def on_submit(self):
        meter_id = self.entry_meter.get().strip()
        
        if not meter_id or not self.selected_package:
            messagebox.showwarning("Error", "Lengkapi Data")
            return
            
        # Validasi Nomor PLN
        import backend.utils.validator as validator
        if not validator.is_valid_pln_number(meter_id):
            messagebox.showwarning("Error", "Nomor Meter Salah!\nHarus 11-12 digit angka.")
            return

        self.transaction_callback("token", {
            "meter": meter_id,
            "nominal": self.selected_package['nominal'],
            "harga": self.selected_package['harga']
        })

class TokenResultView(ctk.CTkFrame):
    def __init__(self, master, token_code, amount, back_to_home_callback):
        super().__init__(master, fg_color=Theme.BG)
        self.token_code = token_code
        self.amount = amount
        self.back_to_home_callback = back_to_home_callback
        
        self.create_widgets()
        
    def create_widgets(self):
        # Kontainer Tengah
        container = ctk.CTkFrame(self, fg_color=Theme.WHITE, corner_radius=20)
        container.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.85, relheight=0.6)
        
        # Ikon Sukses
        ctk.CTkLabel(container, text="✅", font=("Arial", 60)).pack(pady=(40, 10))
        ctk.CTkLabel(container, text="Transaksi Berhasil", font=Theme.F_HEAD, text_color=Theme.PRIMARY).pack(pady=(0, 20))
        
        # Nomor Token (Diformat 4-4-4-4-4)
        formatted_token = " ".join([self.token_code[i:i+4] for i in range(0, len(self.token_code), 4)])
        
        token_label = ctk.CTkLabel(container, text=formatted_token, font=("Courier", 24, "bold"), text_color=Theme.TEXT)
        token_label.pack(pady=20)
        
        # Info Salin
        ctk.CTkLabel(container, text="Nomor Token Listrik", font=Theme.F_SMALL, text_color=Theme.MUTED).pack()
        
        # Amount
        ctk.CTkLabel(container, text=f"Nominal: Rp {self.amount:,}".replace(",", "."), 
                     font=Theme.F_BODY, text_color=Theme.TEXT).pack(pady=(20, 0))

        # Tombol Beranda
        ctk.CTkButton(container, text="Selesai", font=Theme.F_BTN,
                      fg_color=Theme.PRIMARY, height=50, corner_radius=10,
                      command=self.back_to_home_callback).pack(side="bottom", fill="x", padx=30, pady=30)