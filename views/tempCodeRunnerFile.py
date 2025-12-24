import tkinter as tk
from tkinter import messagebox
import sys, os


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from theme import Theme, draw_rounded_rect, draw_icon, draw_nav_icon

class HomeView:
    def __init__(self, canvas, width, height, on_navigate):
        self.canvas, self.W, self.H, self.navigate = canvas, width, height, on_navigate

    def draw(self):
        self.canvas.delete("all")
        
        # --- HEADER ---
        self.canvas.create_rectangle(0, 0, self.W, 260, fill=Theme.PRIMARY, outline="")
        self.draw_btn_avatar(50, 70, "A", lambda: self.navigate("profile"))
        
        self.canvas.create_text(110, 70, text="Halo, Ahmad", anchor="w", font=Theme.F_HEAD, fill=Theme.WHITE)
        self.canvas.create_text(110, 95, text="Gold Member", anchor="w", font=Theme.F_SMALL, fill="#E8F5E9")
        
        self.canvas.create_oval(self.W-60, 70, self.W-50, 80, fill=Theme.IC_RED, outline=Theme.WHITE, width=2)
        self.canvas.create_text(self.W-70, 75, text="Notif", anchor="e", font=Theme.F_SMALL, fill=Theme.WHITE)

        # --- LOGIKA KEUANGAN ---
        limit, masuk, saldo = 40000000, 5000000, 2500000
        keluar = masuk - saldo
        
        # Hitung Persen & Format String
        p_masuk = int((masuk / limit) * 100)
        p_keluar = int((keluar / masuk) * 100)
        str_saldo = f"Rp {saldo:,.0f}".replace(",", ".")

        # ---  KARTU SALDO ---
        draw_rounded_rect(self.canvas, 40, 145, self.W-40, 315, 25, Theme.SHADOW)
        draw_rounded_rect(self.canvas, 40, 140, self.W-40, 310, 25, Theme.WHITE)
        self.canvas.create_text(70, 185, text="Total Saldo Aktif", anchor="w", font=Theme.F_BODY, fill=Theme.MUTED)
        self.canvas.create_text(70, 235, text=str_saldo, anchor="w", font=Theme.F_SALDO, fill=Theme.TEXT)

        # --- KARTU STATISTIK ---
        y, w = 340, (self.W - 100) / 2
        self.draw_stat_card(40, y, w, "Pemasukan", masuk, Theme.INCOME, "up", p_masuk)
        self.draw_stat_card(40+w+20, y, w, "Pengeluaran", keluar, Theme.EXPENSE, "down", p_keluar)

        # ---  MENU LAYANAN ---
        self.canvas.create_text(40, 530, text="Layanan Keuangan", anchor="w", font=Theme.F_TITLE, fill=Theme.TEXT)
        menus = [
            ("Top Up", Theme.BTN_GREEN, Theme.IC_GREEN, "plus", "fitur_topup"),
            ("Transfer", Theme.BTN_BLUE, Theme.IC_BLUE, "arrow_r", "fitur_transfer"),
            ("Tarik", Theme.BTN_ORANGE, Theme.IC_ORANGE, "arrow_d", "fitur_tarik"),
            ("Pulsa", Theme.BTN_RED, Theme.IC_RED, "phone", "fitur_pulsa"),
            ("Listrik", Theme.BTN_YELLOW, Theme.IC_YELLOW, "lightning", "fitur_listrik"),
            ("Lainnya", Theme.BTN_PURPLE, Theme.IC_PURPLE, "dots", None)
        ]

        col_w, y_menu = self.W / 3, 600
        for i, (lbl, bg, col, icon, cmd) in enumerate(menus):
            x = ((i % 3) * col_w) + (col_w / 2)
            y = y_menu + ((i // 3) * 110)
            tag = f"btn_{lbl}"
            
            self.draw_btn_menu(x, y, bg, col, icon, lbl, tag)
            action = lambda e, t=cmd: self.navigate(t) if t else messagebox.showinfo("Info", "Belum tersedia")
            self.canvas.tag_bind(tag, "<Button-1>", action)

        # ---  NAVIGASI BAWAH ---
        self.draw_bottom_nav()

    # --- HELPERS (Fungsi Gambar) ---

    def draw_stat_card(self, x, y, w, title, val, color, arrow, pct):
        draw_rounded_rect(self.canvas, x, y, x+w, y+150, 20, Theme.WHITE)
        
        # Icon Panah
        self.canvas.create_oval(x+20, y+20, x+50, y+50, fill=Theme.BG, outline="")
        cx, cy = x+35, y+35
        pts = [cx, cy+6, cx, cy-6, cx-4, cy-2, cx, cy-6, cx+4, cy-2, cx, cy-6] if arrow=="up" else \
              [cx, cy-6, cx, cy+6, cx-4, cy+2, cx, cy+6, cx+4, cy+2, cx, cy+6]
        self.canvas.create_line(pts, fill=color, width=2)

        # Teks
        amount = f"Rp {val:,.0f}".replace(",", ".")
        self.canvas.create_text(x+20, y+75, text=title, anchor="w", font=Theme.F_BODY, fill=Theme.MUTED)
        self.canvas.create_text(x+20, y+100, text=amount, anchor="w", font=Theme.F_JUMBO, fill=Theme.TEXT)
        
        # Stik Bar
        bx1, by1, bx2, by2 = x+20, y+130, x+w-20, y+135
        draw_rounded_rect(self.canvas, bx1, by1, bx2, by2, 2, "#E0E0E0")
        if pct > 0:
            fw = (bx2-bx1) * (min(pct, 100)/100)
            draw_rounded_rect(self.canvas, bx1, by1, bx1+fw, by2, 2, color)
        self.canvas.create_text(bx2, by1-10, text=f"{pct}%", anchor="e", font=("Arial", 9, "bold"), fill=color)

    def draw_btn_menu(self, x, y, bg, col, icon, lbl, tag):
        self.canvas.create_oval(x-35, y-35, x+35, y+35, fill=bg, outline="", tags=tag)
        draw_icon(self.canvas, x, y, icon, col)
        self.canvas.create_text(x, y+50, text=lbl, font=Theme.F_BTN, fill=Theme.TEXT, tags=tag)
        self.add_hover(tag)

    def draw_btn_avatar(self, x, y, char, cmd):
        tag = "btn_avatar"
        self.canvas.create_oval(x-30, y-30, x+30, y+30, fill=Theme.WHITE, outline="", tags=tag)
        self.canvas.create_text(x, y, text=char, font=("Arial", 20, "bold"), fill=Theme.PRIMARY, tags=tag)
        self.canvas.tag_bind(tag, "<Button-1>", lambda e: cmd())
        self.add_hover(tag)

    def draw_bottom_nav(self):
        y_bg, cw = self.H - 90, self.W / 3
        self.canvas.create_rectangle(0, y_bg, self.W, self.H, fill=Theme.WHITE, outline="#EEEEEE")
        
        navs = [("Home","home",None), ("Riwayat","history","history"), ("Setelan","settings","profile")]
        for i, (lbl, icon, target) in enumerate(navs):
            x = (i * cw) + (cw / 2)
            col = Theme.PRIMARY if i == 0 else "#CFD8DC"
            tag = f"nav_{lbl}"
            draw_nav_icon(self.canvas, x, self.H-55, icon, col, tag)
            self.canvas.create_text(x, self.H-25, text=lbl, font=Theme.F_SMALL, fill=col, tags=tag)
            if target:
                self.canvas.tag_bind(tag, "<Button-1>", lambda e, t=target: self.navigate(t))
                self.add_hover(tag)

    def add_hover(self, tag):
        self.canvas.tag_bind(tag, "<Enter>", lambda e: self.canvas.config(cursor="hand2"))
        self.canvas.tag_bind(tag, "<Leave>", lambda e: self.canvas.config(cursor=""))