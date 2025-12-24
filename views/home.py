import tkinter as tk
from tkinter import messagebox
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from theme import Theme, draw_rounded_rect, draw_icon, draw_nav_icon

class HomeView:
    def __init__(self, canvas, width, height, on_navigate):
        self.canvas = canvas
        self.W = width
        self.H = height
        self.navigate = on_navigate 

    def draw(self):
        self.canvas.delete("all")
        
        # --- HEADER ---
        self.canvas.create_rectangle(0, 0, self.W, 260, fill=Theme.PRIMARY, outline="")
        
        self.draw_btn_avatar(50, 70, "A", cmd=lambda: self.navigate("profile"))
        self.canvas.create_text(110, 70, text="Halo, Ahmad", anchor="w", font=Theme.F_HEAD, fill=Theme.WHITE)
        self.canvas.create_text(110, 95, text="Gold Member", anchor="w", font=Theme.F_SMALL, fill="#E8F5E9")
        
        self.canvas.create_oval(self.W-60, 70, self.W-50, 80, fill=Theme.IC_RED, outline=Theme.WHITE, width=2)
        self.canvas.create_text(self.W-70, 75, text="Notif", anchor="e", font=Theme.F_SMALL, fill=Theme.WHITE)

        limit_max_dana = 40000000 
        
        pemasukan_real = 5000000  
        saldo_saat_ini = 2500000  
        
        pengeluaran_real = pemasukan_real - saldo_saat_ini

        str_saldo = f"Rp {saldo_saat_ini:,.0f}".replace(",", ".")
        str_masuk = f"Rp {pemasukan_real:,.0f}".replace(",", ".")
        str_keluar = f"Rp {pengeluaran_real:,.0f}".replace(",", ".")
        persen_masuk = int((pemasukan_real / limit_max_dana) * 100)
        
        persen_keluar = int((pengeluaran_real / pemasukan_real) * 100)


        # --- KARTU SALDO ---
        draw_rounded_rect(self.canvas, 40, 145, self.W-40, 315, 25, Theme.SHADOW)
        draw_rounded_rect(self.canvas, 40, 140, self.W-40, 310, 25, Theme.WHITE)
        
        self.canvas.create_text(70, 185, text="Total Saldo Aktif", anchor="w", font=Theme.F_BODY, fill=Theme.MUTED)
        self.canvas.create_text(70, 235, text=str_saldo, anchor="w", font=Theme.F_SALDO, fill=Theme.TEXT)

        # --- KARTU STATISTIK ---
        y_stats = 340
        card_w = (self.W - 100) / 2
        
        self.draw_card_stats(40, y_stats, card_w, "Pemasukan", str_masuk, Theme.INCOME, "up", persen_masuk)
        self.draw_card_stats(40 + card_w + 20, y_stats, card_w, "Pengeluaran", str_keluar, Theme.EXPENSE, "down", persen_keluar)

        # --- MENU GRID ---
        self.canvas.create_text(40, 530, text="Layanan Keuangan", anchor="w", font=Theme.F_TITLE, fill=Theme.TEXT)
        
        daftar_menu = [
            ("Top Up",   Theme.BTN_GREEN,  Theme.IC_GREEN,  "plus",      "fitur_topup"),
            ("Transfer", Theme.BTN_BLUE,   Theme.IC_BLUE,   "arrow_r",   "fitur_transfer"),
            ("Tarik",    Theme.BTN_ORANGE, Theme.IC_ORANGE, "arrow_d",   "fitur_tarik"),
            ("Pulsa",    Theme.BTN_RED,    Theme.IC_RED,    "phone",     "fitur_pulsa"),
            ("Listrik",  Theme.BTN_YELLOW, Theme.IC_YELLOW, "lightning", "fitur_listrik"),
            ("Lainnya",  Theme.BTN_PURPLE, Theme.IC_PURPLE, "dots",      None) 
        ]

        col_w = self.W / 3
        y_awal = 600
        
        for i, item in enumerate(daftar_menu):
            label, bg, ic_col, ic_type, tujuan = item
            row = i // 3; col = i % 3
            x = (col * col_w) + (col_w / 2)
            y = y_awal + (row * 110)
            
            tag = f"btn_{label}"
            self.draw_btn_menu(x, y, bg, ic_col, ic_type, label, tag)
            
            if tujuan:
                self.canvas.tag_bind(tag, "<Button-1>", lambda e, t=tujuan: self.navigate(t))
            else:
                self.canvas.tag_bind(tag, "<Button-1>", lambda e: messagebox.showinfo("Info", "Maaf belum tersedia"))

        # --- NAVIGASI BAWAH ---
        self.draw_bottom_nav()

    # --- HELPERS ---

    def draw_card_stats(self, x, y, w, title, amount, color, arrow, percent):
        h = 150
        draw_rounded_rect(self.canvas, x, y, x+w, y+h, 20, Theme.WHITE)
        
        self.canvas.create_oval(x+20, y+20, x+50, y+50, fill=Theme.BG, outline="")
        cx, cy = x+35, y+35
        if arrow == "up":
            pts = [cx, cy+6, cx, cy-6, cx-4, cy-2, cx, cy-6, cx+4, cy-2, cx, cy-6]
        else:
            pts = [cx, cy-6, cx, cy+6, cx-4, cy+2, cx, cy+6, cx+4, cy+2, cx, cy+6]
        self.canvas.create_line(pts, fill=color, width=2)

        self.canvas.create_text(x+20, y+75, text=title, anchor="w", font=Theme.F_BODY, fill=Theme.MUTED)
        self.canvas.create_text(x+20, y+100, text=amount, anchor="w", font=Theme.F_JUMBO, fill=Theme.TEXT)
        
        # Stik Bar
        bar_x1, bar_y1 = x + 20, y + 130
        bar_x2, bar_y2 = x + w - 20, y + 135
        draw_rounded_rect(self.canvas, bar_x1, bar_y1, bar_x2, bar_y2, 2, "#E0E0E0") 
        
        if percent > 0:
            fill_w = (bar_x2 - bar_x1) * (percent / 100)
            if percent > 100: fill_w = bar_x2 - bar_x1
            draw_rounded_rect(self.canvas, bar_x1, bar_y1, bar_x1 + fill_w, bar_y2, 2, color)
        
        self.canvas.create_text(bar_x2, bar_y1 - 10, text=f"{percent}%", anchor="e", font=("Arial", 9, "bold"), fill=color)

    def draw_btn_menu(self, x, y, bg, ic_col, ic_type, label, tag):
        r = 35
        self.canvas.create_oval(x-r, y-r, x+r, y+r, fill=bg, outline="", tags=tag)
        draw_icon(self.canvas, x, y, ic_type, ic_col)
        self.canvas.create_text(x, y+50, text=label, font=Theme.F_BTN, fill=Theme.TEXT, tags=tag)
        self.efek_hover(tag)

    def draw_btn_avatar(self, x, y, char, cmd):
        tag = "btn_avatar"
        self.canvas.create_oval(x-30, y-30, x+30, y+30, fill=Theme.WHITE, outline="", tags=tag)
        self.canvas.create_text(x, y, text=char, font=("Arial", 20, "bold"), fill=Theme.PRIMARY, tags=tag)
        self.canvas.tag_bind(tag, "<Button-1>", lambda e: cmd())
        self.efek_hover(tag)

    def draw_bottom_nav(self):
        y_bg = self.H - 90
        self.canvas.create_rectangle(0, y_bg, self.W, self.H, fill=Theme.WHITE, outline="#EEEEEE")
        
        items = [("Home","home",None), ("Riwayat","history","history"), ("Setelan","settings","profile")]
        cw = self.W / 3
        y_icon = self.H - 55
        
        for i, (lbl, icon, target) in enumerate(items):
            x = (i * cw) + (cw / 2)
            color = Theme.PRIMARY if i == 0 else "#CFD8DC"
            tag = f"nav_{lbl}"
            draw_nav_icon(self.canvas, x, y_icon, icon, color, tag=tag)
            self.canvas.create_text(x, y_icon+30, text=lbl, font=Theme.F_SMALL, fill=color, tags=tag)
            
            if target:
                self.canvas.tag_bind(tag, "<Button-1>", lambda e, t=target: self.navigate(t))
                self.efek_hover(tag)

    def efek_hover(self, tag):
        self.canvas.tag_bind(tag, "<Enter>", lambda e: self.canvas.config(cursor="hand2"))
        self.canvas.tag_bind(tag, "<Leave>", lambda e: self.canvas.config(cursor=""))