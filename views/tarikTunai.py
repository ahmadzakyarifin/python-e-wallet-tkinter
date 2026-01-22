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

class WithdrawView(ctk.CTkFrame):
    def __init__(self, master, user_data, navigate_callback, withdraw_callback):
        super().__init__(master, fg_color=Theme.BG)
        self.user_data = user_data
        self.navigate_callback = navigate_callback
        self.withdraw_callback = withdraw_callback
        self.biaya_admin = 4500 # Adjusted to specific case
        self.create_widgets()

    def create_widgets(self):
        # 1. HEADER STANDAR
        header = ctk.CTkFrame(self, fg_color=Theme.PRIMARY, height=80, corner_radius=0)
        header.pack(fill="x", anchor="n")
        
        ctk.CTkButton(header, text="←", font=("Arial", 24, "bold"), fg_color=Theme.WHITE, text_color=Theme.PRIMARY,
                      width=40, height=40, corner_radius=20, cursor="hand2", hover_color=Theme.BTN_HOVER_LIGHT,
                      command=lambda: self.navigate_callback("home")).pack(side="left", padx=20, pady=10)

        ctk.CTkLabel(header, text="Tarik Tunai", font=("Arial", 18, "bold"), text_color=Theme.WHITE).pack(side="left", padx=10)
        
        saldo = f"Rp {self.user_data.get('saldo', 0):,}".replace(",", ".")
        ctk.CTkLabel(header, text=f"Saldo: {saldo}", font=("Arial", 12), text_color="#E8F5E9").pack(side="right", padx=20)

        # 2. KONTEN SCROLL
        self.scroll = ctk.CTkScrollableFrame(self, fg_color=Theme.BG)
        self.scroll.pack(fill="both", expand=True)

        # 3. INFO
        info = ctk.CTkFrame(self.scroll, fg_color="#E8F5E9", corner_radius=10, border_width=1, border_color="#C8E6C9")
        info.pack(fill="x", padx=20, pady=(20, 10))
        ctk.CTkLabel(info, text="ℹ️ Tarik tunai tanpa kartu di ATM BCA, BNI, BRI & Indomaret", 
                     text_color=Theme.PRIMARY, font=("Arial", 11)).pack(padx=15, pady=15, anchor="w")

        # 4. KARTU INPUT
        card = ctk.CTkFrame(self.scroll, fg_color=Theme.WHITE, corner_radius=15)
        card.pack(fill="x", padx=20, pady=10)

        # Input Nominal
        ctk.CTkLabel(card, text="Nominal Penarikan", font=("Arial", 12, "bold"), text_color=Theme.TEXT).pack(anchor="w", padx=20, pady=(20, 5))
        self.entry_nominal = ctk.CTkEntry(card, placeholder_text="Rp 0", height=50, border_width=0, 
                                          fg_color="#F0F0F0", text_color=Theme.TEXT, font=("Arial", 16, "bold"))
        self.entry_nominal.pack(fill="x", padx=20, pady=(0, 15))
        self.entry_nominal.bind("<KeyRelease>", self.format_rupiah)

        # Aksi Cepat
        q_frame = ctk.CTkFrame(card, fg_color="transparent")
        q_frame.pack(fill="x", padx=20, pady=(0, 20))
        for amt in [100000, 200000, 500000, 1000000]:
            txt = f"{amt//1000}k" if amt < 1000000 else "1jt"
            ctk.CTkButton(q_frame, text=txt, width=60, height=35, 
                          fg_color=Theme.BTN_LIGHT, text_color=Theme.TEXT, 
                          border_width=0, cursor="hand2", hover_color=Theme.BTN_HOVER_LIGHT,
                          command=lambda x=amt: self.set_nominal(x)).pack(side="left", padx=(0,10), expand=True, fill="x")

        # PILIH LOKASI (Gaya Kartu, bukan Dropdown)
        ctk.CTkLabel(card, text="Pilih Lokasi Penarikan", font=("Arial", 12, "bold"), text_color=Theme.TEXT).pack(anchor="w", padx=20, pady=(0, 5))
        
        self.loc_buttons = []
        self.selected_loc = None
        
        locs = [
            {"name": "ATM BCA", "fee": 0},
            {"name": "ATM Lain", "fee": 6500},
            {"name": "Indomaret", "fee": 4500},
            {"name": "Alfamart", "fee": 4500},
        ]
        
        grid = ctk.CTkFrame(card, fg_color="transparent")
        grid.pack(fill="x", padx=20, pady=(0, 15))
        
        for i, l in enumerate(locs):
            self.create_loc_btn(grid, l, i)

        # Info Biaya Admin
        self.lbl_fee = ctk.CTkLabel(card, text="Biaya Admin: Rp -", text_color="#F57C00", font=("Arial", 12, "bold"))
        self.lbl_fee.pack(padx=20, pady=(0, 20), anchor="w")

        # 5. AKSI TOMBOL
        ctk.CTkButton(self.scroll, text="BUAT KODE PENARIKAN", font=Theme.F_BTN,
                      fg_color=Theme.PRIMARY, height=50, corner_radius=10, 
                      cursor="hand2", hover_color=Theme.BTN_HOVER_DARK,
                      command=self.on_submit).pack(fill="x", padx=20, pady=30)
    
    def create_loc_btn(self, parent, item, idx):
        # 2 kolom layout
        row = idx // 2
        col = idx % 2
        
        btn = ctk.CTkButton(parent, text=f"{item['name']}\nRp {item['fee']:,}", 
                            font=("Arial", 12), fg_color="#F0F0F0", text_color=Theme.TEXT,
                            width=100, height=50, border_width=1, border_color="#E0E0E0",
                            cursor="hand2", hover_color=Theme.BTN_HOVER_LIGHT,
                            command=lambda: self.select_loc(item, btn))
        btn.grid(row=row, column=col, padx=5, pady=5, sticky="ew")
        parent.grid_columnconfigure(0, weight=1)
        parent.grid_columnconfigure(1, weight=1)
        self.loc_buttons.append(btn)

    def select_loc(self, item, btn_obj):
        self.selected_loc = item['name']
        self.biaya_admin = item['fee']
        self.lbl_fee.configure(text=f"Biaya Admin: Rp {self.biaya_admin:,}".replace(",", "."))
        
        for b in self.loc_buttons:
            b.configure(fg_color="#F0F0F0", border_color="#E0E0E0", text_color=Theme.TEXT)
        btn_obj.configure(fg_color="#E8F5E9", border_color=Theme.PRIMARY, text_color=Theme.PRIMARY)

    def format_rupiah(self, event):
        val = self.entry_nominal.get().replace(".", "")
        if val.isdigit():
            self.entry_nominal.delete(0, "end")
            self.entry_nominal.insert(0, f"{int(val):,}".replace(",", "."))

    def set_nominal(self, x):
        self.entry_nominal.delete(0, "end")
        self.entry_nominal.insert(0, f"{x:,}".replace(",", "."))

    def on_submit(self):
        val = self.entry_nominal.get().replace(".", "")
        if not val.isdigit() or int(val) < 50000:
            messagebox.showwarning("Error", "Minimal Rp 50.000")
            return
        
        if not self.selected_loc:
            messagebox.showwarning("Error", "Pilih Lokasi Penarikan")
            return

        kode = self.withdraw_callback(int(val), self.biaya_admin, self.selected_loc)
        if kode:
            self.show_success(kode, int(val), self.selected_loc)

    def show_success(self, kode, nominal, lokasi):
        # Format Kode: 123456 -> 123 456
        fmt_kode = " ".join([kode[i:i+3] for i in range(0, len(kode), 3)])
        
        win = ctk.CTkToplevel(self)
        win.title("Kode Penarikan")
        win.geometry("400x550")
        win.resizable(False, False)
        
        # FIX CRASH: Wait for window to be visible before grabbing focus
        win.lift()
        win.focus_force()
        # win.grab_set() # Optional, sometimes causes issues if too fast. Let's rely on focus.

        # Container Utama (Putih)
        bg = ctk.CTkFrame(win, fg_color="white", corner_radius=0)
        bg.pack(fill="both", expand=True)

        # Header
        ctk.CTkLabel(bg, text="Kode Penarikan", font=("Arial", 18, "bold"), text_color="#333").pack(pady=(25, 5))
        ctk.CTkLabel(bg, text=f"Merchant: {lokasi.split(' ')[-1]}", font=("Arial", 12), text_color="gray").pack()

        # Kartu Kode (Tengah)
        # Visual Barcode (Simulasi dengan garis-garis)
        barcode_frame = ctk.CTkFrame(bg, fg_color="transparent")
        barcode_frame.pack(pady=(30, 10))
        
        # Drawing fake barcode using frame stripes
        for _ in range(25):
            w = 2 if _ % 3 == 0 else 4
            h = 60
            f = ctk.CTkFrame(barcode_frame, width=w, height=h, fg_color="#333", corner_radius=0)
            f.pack(side="left", padx=1)

        ctk.CTkLabel(bg, text=fmt_kode, font=("Arial", 32, "bold"), text_color=Theme.PRIMARY).pack(pady=(10, 5))
        
        # Info Berlaku
        limit_time = "15 Menit" # In real app, calculate actual time
        ctk.CTkLabel(bg, text=f"Berlaku dalam {limit_time}", font=("Arial", 12), text_color="#F57C00").pack(pady=(0, 20))

        # Instructions
        note_frame = ctk.CTkFrame(bg, fg_color="#F1F8E9", corner_radius=10)
        note_frame.pack(fill="x", padx=30, pady=10)
        
        steps = [
            f"1. Pergi ke kasir/ATM {lokasi}",
            "2. Info 'Tarik Tunai Tanpa Kartu'",
            "3. Tunjukkan Kode Penarikan",
            f"4. Ambil uang Rp {nominal:,}".replace(",", ".")
        ]
        
        for step in steps:
            ctk.CTkLabel(note_frame, text=step, font=("Arial", 12), text_color="#333", anchor="w").pack(fill="x", padx=15, pady=3)

        # Tombol Tutup
        ctk.CTkButton(bg, text="TUTUP", font=Theme.F_BTN, fg_color=Theme.PRIMARY, height=50, corner_radius=25,
                      hover_color=Theme.BTN_HOVER,
                      command=lambda: [win.destroy(), self.navigate_callback("home")]).pack(side="bottom", fill="x", padx=30, pady=30)