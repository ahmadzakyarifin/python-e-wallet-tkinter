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
        PRIMARY = "#05B048"
        TEXT = "#333333"
        MUTED = "#888888"
        BTN_GREEN = "#05B048"
        BTN_HOVER = "#008e36"
        F_HEAD = ("Arial", 16, "bold")
        F_BODY = ("Arial", 12)
        F_BTN = ("Arial", 12, "bold")

class TransferView(ctk.CTkFrame):
    def __init__(self, master, user_data, navigate_callback, transfer_callback):
        super().__init__(master, fg_color=Theme.BG)
        self.user_data = user_data
        self.navigate_callback = navigate_callback
        self.transfer_callback = transfer_callback
        self.create_widgets()

    def create_widgets(self):
        # 1. HEADER STANDARD
        header = ctk.CTkFrame(self, fg_color=Theme.PRIMARY, height=80, corner_radius=0)
        header.pack(fill="x", anchor="n")
        
        ctk.CTkButton(header, text="←", font=("Arial", 24, "bold"), fg_color=Theme.WHITE, text_color=Theme.PRIMARY,
                      width=40, height=40, corner_radius=20, cursor="hand2", hover_color=Theme.BTN_HOVER_LIGHT,
                      command=lambda: self.navigate_callback("home")).pack(side="left", padx=20, pady=10)

        ctk.CTkLabel(header, text="Transfer Saldo", font=("Arial", 18, "bold"), text_color=Theme.WHITE).pack(side="left", padx=10)
        
        saldo = f"Rp {self.user_data.get('saldo', 0):,}".replace(",", ".")
        ctk.CTkLabel(header, text=f"Saldo: {saldo}", font=("Arial", 12), text_color="#E8F5E9").pack(side="right", padx=20)

        # 2. SCROLL CONTENT
        self.scroll = ctk.CTkScrollableFrame(self, fg_color=Theme.BG)
        self.scroll.pack(fill="both", expand=True)

        # 3. CARD INPUT
        card = ctk.CTkFrame(self.scroll, fg_color=Theme.WHITE, corner_radius=15)
        card.pack(fill="x", padx=20, pady=20)

        # Input Nomor
        ctk.CTkLabel(card, text="Nomor Tujuan", font=("Arial", 12, "bold"), text_color=Theme.TEXT).pack(anchor="w", padx=20, pady=(20, 5))
        self.entry_nomor = ctk.CTkEntry(card, placeholder_text="08xx / ID E-Saku", height=50, border_width=0, 
                                        fg_color="#F0F0F0", text_color=Theme.TEXT, font=("Arial", 14))
        self.entry_nomor.pack(fill="x", padx=20, pady=(0, 15))

        # Input Nominal
        ctk.CTkLabel(card, text="Nominal Transfer", font=("Arial", 12, "bold"), text_color=Theme.TEXT).pack(anchor="w", padx=20, pady=(0, 5))
        self.entry_nominal = ctk.CTkEntry(card, placeholder_text="Rp 0", height=50, border_width=0, 
                                          fg_color="#F0F0F0", text_color=Theme.TEXT, font=("Arial", 16, "bold"))
        self.entry_nominal.pack(fill="x", padx=20, pady=(0, 15))
        self.entry_nominal.bind("<KeyRelease>", self.format_rupiah)
        
        # Input Catatan
        ctk.CTkLabel(card, text="Catatan (Opsional)", font=("Arial", 12, "bold"), text_color=Theme.MUTED).pack(anchor="w", padx=20, pady=(0, 5))
        self.entry_catatan = ctk.CTkEntry(card, placeholder_text="Bayar hutang...", height=50, border_width=0, 
                                          fg_color="#F0F0F0", text_color=Theme.TEXT, font=("Arial", 14))
        self.entry_catatan.pack(fill="x", padx=20, pady=(0, 20))

        # Quick Actions
        q_frame = ctk.CTkFrame(card, fg_color="transparent")
        q_frame.pack(fill="x", padx=20, pady=(0, 20))
        for amt in [50000, 100000, 200000, 500000]:
            ctk.CTkButton(q_frame, text=f"{amt//1000}k", width=60, height=35, 
                          fg_color=Theme.BTN_LIGHT, text_color=Theme.TEXT, 
                          border_width=0, cursor="hand2", hover_color=Theme.BTN_HOVER_LIGHT,
                          command=lambda x=amt: self.set_nominal(x)).pack(side="left", padx=(0,10), expand=True, fill="x")

        # Admin Fee Info (GRATIS)
        fee_box = ctk.CTkFrame(card, fg_color="#E8F5E9", corner_radius=8)
        fee_box.pack(fill="x", padx=20, pady=(0, 20))
        ctk.CTkLabel(fee_box, text="Biaya Admin: Rp 0 (Gratis)", 
                     text_color=Theme.PRIMARY, font=("Arial", 12, "bold")).pack(padx=15, pady=10)

        # 4. HISTORY SECTION
        self.create_history()

        # 5. BUTTON ACTION
        ctk.CTkButton(self.scroll, text="KIRIM SEKARANG", font=Theme.F_BTN,
                      fg_color=Theme.PRIMARY, height=50, corner_radius=10, 
                      cursor="hand2", hover_color=Theme.BTN_HOVER_DARK,
                      command=self.on_submit).pack(fill="x", padx=20, pady=30)

    def create_history(self):
        ctk.CTkLabel(self.scroll, text="Transfer Terakhir", font=("Arial", 14, "bold"), text_color=Theme.TEXT).pack(anchor="w", padx=20, pady=(0, 10))
        
        riwayat = self.user_data.get('riwayat_transaksi', [])
        recent = []
        seen = set()
        
        for tx in riwayat:
            try:
                # SAFE ACCESS (Dict from to_dict)
                tipe = tx.get('type') 
                desc = tx.get('title', '')
                tgl = tx.get('date', '')
                
                # Filter: Tipe OUT dan Deskripsi mengandung "Transfer ke"
                # Filter: Tipe OUT dan Deskripsi mengandung "Transfer ke"
                if tipe == "out" and "Transfer ke" in desc:
                    parts = desc.split()
                    if len(parts) >= 3:
                        num = parts[2]
                        name_display = "User"

                        # Coba ekstraksi nama dlm kurung: "Transfer ke 08xx (Budi)"
                        if "(" in desc and ")" in desc:
                            try:
                                # Ambil string di antara kurung pertama
                                start = desc.find("(") + 1
                                end = desc.find(")")
                                if end > start:
                                    name_display = desc[start:end]
                            except:
                                pass
                        
                        if num not in seen:
                            recent.append({"nomor": num, "name": name_display})
                            seen.add(num)
            except: continue
            if len(recent) >= 3: break
            
        if not recent:
            ctk.CTkLabel(self.scroll, text="Belum ada riwayat", text_color=Theme.MUTED).pack(padx=20, anchor="w")
            return

        # HORIZONTAL SCROLL CONTAINER
        h_scroll = ctk.CTkScrollableFrame(self.scroll, height=130, orientation="horizontal", fg_color="transparent")
        h_scroll.pack(fill="x", padx=10, pady=5)
            
        for r in recent:
            # Card Container
            card = ctk.CTkFrame(h_scroll, width=110, height=120, fg_color=Theme.WHITE, corner_radius=10)
            card.pack(side="left", padx=5, pady=5)
            card.pack_propagate(False) # Fixed size
            card.configure(cursor="hand2")
            
            # Avatar Icon
            icon_canvas = ctk.CTkCanvas(card, width=40, height=40, bg=Theme.WHITE, highlightthickness=0)
            icon_canvas.pack(pady=(15, 5))
            # Draw Circle
            icon_canvas.create_oval(2, 2, 38, 38, fill=Theme.INPUT_BG, outline=Theme.PRIMARY, width=2)
            # Draw Initial
            initial = r['name'][0] if r['name'] != "Unknown" else "?"
            icon_canvas.create_text(20, 20, text=initial, font=("Arial", 14, "bold"), fill=Theme.PRIMARY)
            
            # Name
            ctk.CTkLabel(card, text=r['name'], font=("Arial", 11, "bold"), text_color=Theme.TEXT).pack()
            # Number
            ctk.CTkLabel(card, text=r['nomor'], font=("Arial", 10), text_color=Theme.MUTED).pack()
            
            # Interaction
            def on_click(n=r['nomor']):
                self.entry_nomor.delete(0, "end")
                self.entry_nomor.insert(0, n)
                
            card.bind("<Button-1>", lambda e, n=r['nomor']: on_click(n))
            for child in card.winfo_children():
                # Bind canvas separately to ensure click works
                if isinstance(child, ctk.CTkCanvas):
                    child.bind("<Button-1>", lambda e, n=r['nomor']: on_click(n))
                else:
                    child.bind("<Button-1>", lambda e, n=r['nomor']: on_click(n))

    def format_rupiah(self, event):
        val = self.entry_nominal.get().replace(".", "")
        if val.isdigit():
            self.entry_nominal.delete(0, "end")
            self.entry_nominal.insert(0, f"{int(val):,}".replace(",", "."))

    def set_nominal(self, x):
        self.entry_nominal.delete(0, "end")
        self.entry_nominal.insert(0, f"{x:,}".replace(",", "."))
        
    def set_nomor(self, n):
        self.entry_nomor.delete(0, "end")
        self.entry_nomor.insert(0, n)

    def on_submit(self):
        nomor = self.entry_nomor.get()
        val = self.entry_nominal.get().replace(".", "")
        if not nomor:
            messagebox.showwarning("Error", "Isi nomor tujuan")
            return
        if not val.isdigit() or int(val) <= 0:
            messagebox.showwarning("Error", "Nominal tidak valid")
            return
        self.transfer_callback(nomor, int(val), self.entry_catatan.get())