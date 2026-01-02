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

class PulsaView(ctk.CTkFrame):
    def __init__(self, master, user_data, navigate_callback, transaction_callback):
        super().__init__(master, fg_color=Theme.BG)
        
        self.user_data = user_data
        self.navigate_callback = navigate_callback
        self.transaction_callback = transaction_callback
        self.selected_operator = None
        self.selected_package = None
        self.op_buttons = []
        self.pkg_buttons = []

        self.create_widgets()

    def create_widgets(self):
        # --- HEADER ---
        header_frame = ctk.CTkFrame(self, fg_color=Theme.PRIMARY, height=80, corner_radius=0)
        header_frame.pack(fill="x", anchor="n")

        btn_back = ctk.CTkButton(header_frame, text="←", font=("Arial", 24, "bold"), 
                                 fg_color=Theme.WHITE, text_color=Theme.PRIMARY,
                                 width=40, height=40, corner_radius=20,
                                 command=lambda: self.navigate_callback("home"))
        btn_back.pack(side="left", padx=20, pady=10)

        title_lbl = ctk.CTkLabel(header_frame, text="Isi Pulsa", font=("Arial", 18, "bold"), text_color=Theme.WHITE)
        title_lbl.pack(side="left", padx=10)

        saldo_txt = f"Rp {self.user_data.get('saldo', 0):,}".replace(",", ".")
        saldo_lbl = ctk.CTkLabel(header_frame, text=f"Saldo: {saldo_txt}", font=("Arial", 12), text_color="#E8F5E9")
        saldo_lbl.pack(side="right", padx=20)

        # --- CONTENT ---
        self.scroll_frame = ctk.CTkScrollableFrame(self, fg_color=Theme.BG)
        self.scroll_frame.pack(fill="both", expand=True)

        card = ctk.CTkFrame(self.scroll_frame, fg_color=Theme.WHITE, corner_radius=15)
        card.pack(fill="x", padx=20, pady=20)

        # 1. Nomor HP
        ctk.CTkLabel(card, text="Nomor HP", font=("Arial", 12, "bold"), text_color=Theme.TEXT).pack(anchor="w", padx=20, pady=(20, 5))
        self.nomor_entry = ctk.CTkEntry(card, placeholder_text="08xx...", height=45, border_width=0, fg_color="#F0F0F0", text_color=Theme.TEXT)
        self.nomor_entry.pack(fill="x", padx=20, pady=(0, 15))

        # 2. Operator
        ctk.CTkLabel(card, text="Operator", font=("Arial", 12, "bold"), text_color=Theme.TEXT).pack(anchor="w", padx=20, pady=(0, 5))
        op_frame = ctk.CTkFrame(card, fg_color="transparent")
        op_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        operators = ["Telkomsel", "Indosat", "XL", "Tri"]
        for op in operators:
            btn = ctk.CTkButton(op_frame, text=op, width=60, height=35, fg_color="#F0F0F0", text_color="#666",
                                command=lambda x=op: self.select_operator(x))
            btn.pack(side="left", padx=(0,5), expand=True, fill="x")
            self.op_buttons.append(btn)

        # 3. Paket Pulsa
        ctk.CTkLabel(card, text="Pilih Nominal", font=("Arial", 12, "bold"), text_color=Theme.TEXT).pack(anchor="w", padx=20, pady=(10, 5))
        
        pulsa_list = [
            {"nominal": 5000, "harga": 6500},
            {"nominal": 10000, "harga": 11500},
            {"nominal": 25000, "harga": 26500},
            {"nominal": 50000, "harga": 51500},
            {"nominal": 100000, "harga": 101500}
        ]
        
        for item in pulsa_list:
            self.create_package_item(card, item)

        # Tombol Beli
        btn_buy = ctk.CTkButton(self.scroll_frame, text="BELI PULSA", font=Theme.F_BTN,
                                fg_color=Theme.BTN_GREEN, height=50, corner_radius=10,
                                command=self.on_buy_pulsa)
        btn_buy.pack(fill="x", padx=20, pady=20)

    # --- LOGIC ---
    def select_operator(self, op_name):
        self.selected_operator = op_name
        for btn in self.op_buttons:
            if btn.cget("text") == op_name:
                btn.configure(fg_color=Theme.BTN_GREEN, text_color="white")
            else:
                btn.configure(fg_color="#F0F0F0", text_color="#666")

    def create_package_item(self, parent, item):
        frame = ctk.CTkFrame(parent, fg_color="white", border_width=1, border_color="#E0E0E0", corner_radius=8)
        frame.pack(fill="x", padx=20, pady=5)
        
        txt_nom = f"Rp {item['nominal']:,}".replace(",", ".")
        ctk.CTkLabel(frame, text=txt_nom, font=("Arial", 12, "bold")).pack(side="left", padx=10, pady=10)
        
        txt_harga = f"Rp {item['harga']:,}".replace(",", ".")
        ctk.CTkLabel(frame, text=txt_harga, font=("Arial", 12, "bold"), text_color=Theme.BTN_GREEN).pack(side="right", padx=10)

        def on_click(e):
            self.selected_package = item
            for btn_f in self.pkg_buttons:
                btn_f.configure(border_color="#E0E0E0", border_width=1)
            frame.configure(border_color=Theme.BTN_GREEN, border_width=2)
            
        frame.bind("<Button-1>", on_click)
        for child in frame.winfo_children():
            child.bind("<Button-1>", on_click)
        self.pkg_buttons.append(frame)

    def on_buy_pulsa(self):
        nomor = self.nomor_entry.get()
        if not nomor or not self.selected_operator or not self.selected_package:
            messagebox.showwarning("Error", "Lengkapi data (Nomor, Operator, Paket)")
            return
            
        self.transaction_callback("pulsa", {
            "nomor": nomor,
            "operator": self.selected_operator,
            "nominal": self.selected_package['nominal'],
            "harga": self.selected_package['harga']
        })