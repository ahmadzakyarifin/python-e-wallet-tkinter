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

class TopUpView(ctk.CTkFrame):
    def __init__(self, master, user_data, navigate_callback, topup_callback):
        super().__init__(master, fg_color=Theme.BG)
        
        self.user_data = user_data
        self.navigate_callback = navigate_callback
        self.topup_callback = topup_callback # Callback ke MainApp
        self.selected_method = None

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

        title_lbl = ctk.CTkLabel(header_frame, text="Top Up Saldo", font=("Arial", 18, "bold"), text_color=Theme.WHITE)
        title_lbl.pack(side="left", padx=10)

        # Info Saldo
        saldo_txt = f"Rp {self.user_data.get('saldo', 0):,}".replace(",", ".")
        saldo_lbl = ctk.CTkLabel(header_frame, text=f"Saldo: {saldo_txt}", font=("Arial", 12), text_color="#E8F5E9")
        saldo_lbl.pack(side="right", padx=20)

        # --- SCROLLABLE CONTENT ---
        self.scroll_frame = ctk.CTkScrollableFrame(self, fg_color=Theme.BG)
        self.scroll_frame.pack(fill="both", expand=True)

        # 1. Form Input
        self.create_form_section()

        # 2. Metode Pembayaran
        self.create_payment_method_section()

        # 3. Info Card
        self.create_info_card()

        # 4. Tombol Aksi
        btn_topup = ctk.CTkButton(self.scroll_frame, text="LANJUTKAN TOP UP", font=Theme.F_BTN,
                                  fg_color=Theme.BTN_GREEN, height=50, corner_radius=10,
                                  command=self.on_submit)
        btn_topup.pack(fill="x", padx=20, pady=30)

    def create_form_section(self):
        card = ctk.CTkFrame(self.scroll_frame, fg_color=Theme.WHITE, corner_radius=15)
        card.pack(fill="x", padx=20, pady=20)

        ctk.CTkLabel(card, text="Nominal Top Up (Rp)", font=("Arial", 12, "bold"), text_color=Theme.TEXT).pack(anchor="w", padx=20, pady=(20, 5))
        
        self.entry_nominal = ctk.CTkEntry(card, placeholder_text="0", height=45, border_width=0, fg_color="#F0F0F0", text_color=Theme.TEXT, font=("Arial", 14))
        self.entry_nominal.pack(fill="x", padx=20, pady=(0, 15))
        self.entry_nominal.bind("<KeyRelease>", self.format_rupiah)

        # Quick Amount
        quick_frame = ctk.CTkFrame(card, fg_color="transparent")
        quick_frame.pack(fill="x", padx=20, pady=(0, 20))
        amounts = [50000, 100000, 200000, 500000]
        for amt in amounts:
            txt = f"{amt//1000}k"
            btn = ctk.CTkButton(quick_frame, text=txt, width=60, height=30, 
                                fg_color="#E8F5E9", text_color=Theme.BTN_GREEN, 
                                border_width=1, border_color=Theme.BTN_GREEN,
                                command=lambda x=amt: self.set_nominal(x))
            btn.pack(side="left", padx=(0, 5), expand=True, fill="x")

    def create_payment_method_section(self):
        ctk.CTkLabel(self.scroll_frame, text="Metode Pembayaran", font=("Arial", 14, "bold"), text_color=Theme.TEXT).pack(anchor="w", padx=20, pady=(0, 10))
        
        methods = [
            {"name": "Transfer Bank", "icon": "🏦", "desc": "BCA, BNI, BRI, Mandiri"},
            {"name": "Virtual Account", "icon": "💳", "desc": "VA Otomatis Cepat"},
            {"name": "Minimarket", "icon": "🏪", "desc": "Indomaret / Alfamart"},
        ]
        
        self.method_buttons = []
        for m in methods:
            self.create_method_item(m)

    def create_method_item(self, method):
        frame = ctk.CTkFrame(self.scroll_frame, fg_color=Theme.WHITE, corner_radius=10, border_width=2, border_color="#E0E0E0")
        frame.pack(fill="x", padx=20, pady=5)
        
        # Icon
        ctk.CTkLabel(frame, text=method['icon'], font=("Arial", 20)).pack(side="left", padx=15, pady=15)
        
        # Info
        info = ctk.CTkFrame(frame, fg_color="transparent")
        info.pack(side="left", fill="both", expand=True)
        ctk.CTkLabel(info, text=method['name'], font=("Arial", 12, "bold"), text_color=Theme.TEXT).pack(anchor="w")
        ctk.CTkLabel(info, text=method['desc'], font=("Arial", 10), text_color=Theme.MUTED).pack(anchor="w")

        # Logic Klik
        def on_click(e):
            self.selected_method = method['name']
            for btn in self.method_buttons:
                btn.configure(border_color="#E0E0E0")
            frame.configure(border_color=Theme.BTN_GREEN)
            
        frame.bind("<Button-1>", on_click)
        for child in frame.winfo_children():
            child.bind("<Button-1>", on_click)
            
        self.method_buttons.append(frame)

    def create_info_card(self):
        info_frame = ctk.CTkFrame(self.scroll_frame, fg_color="#E3F2FD", corner_radius=10, border_width=1, border_color="#90CAF9")
        info_frame.pack(fill="x", padx=20, pady=(20, 0))
        
        inner = ctk.CTkFrame(info_frame, fg_color="transparent")
        inner.pack(padx=10, pady=10)
        
        ctk.CTkLabel(inner, text="ℹ️", font=("Arial", 20)).pack(side="left", padx=(0, 10))
        ctk.CTkLabel(inner, text="Saldo akan masuk otomatis setelah\npembayaran dikonfirmasi (1-5 menit)", 
                     font=("Arial", 11), text_color="#1976D2", justify="left").pack(side="left")

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
        if nominal < 10000:
            messagebox.showwarning("Error", "Minimal Top Up Rp 10.000")
            return
            
        if not self.selected_method:
            messagebox.showwarning("Error", "Pilih metode pembayaran")
            return
            
        # Panggil Callback ke MainApp
        self.topup_callback(nominal, self.selected_method)