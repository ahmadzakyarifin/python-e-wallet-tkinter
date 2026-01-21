import tkinter as tk
from tkinter import messagebox
import sys, os
import customtkinter as ctk

# Pengaturan Jalur Tema
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from theme import Theme, draw_rounded_rect, draw_icon, draw_nav_icon

class HistoryView:
    def __init__(self, canvas, width, height, on_navigate, data_transaksi):
        self.canvas = canvas
        self.W = width
        self.H = height
        self.navigate = on_navigate
        
        # Data Diterima dari MainApp (Backend)
        self.data_transaksi = data_transaksi 
        self.widgets = [] 
        
        self.var_search = tk.StringVar()
        self.filter_selected = "Semua" # Default

    def draw(self):
        self.clear_screen()
        
        # --- A. HEADER ---
        self.canvas.create_rectangle(0, 0, self.W, 120, fill=Theme.PRIMARY, outline="")
        self.canvas.create_text(self.W/2, 60, text="Riwayat Transaksi", font=Theme.F_HEAD, fill=Theme.WHITE)
        
        # Background Abu-abu
        self.canvas.create_rectangle(0, 120, self.W, self.H, fill="#FAFAFA", outline="")

        # --- B. UI PENCARIAN & FILTER ---
        self.draw_search_filter_ui(y_pos=140)

        # --- C. RENDER LIST ---
        self.render_list()
        
        # --- D. NAVIGASI BAWAH ---
        self.draw_bottom_nav()

    def draw_search_filter_ui(self, y_pos):
        # Background Input
        bg_input = "#F0F0F0"
        w_search = self.W - 80 
        
        # 1. KOTAK SEARCH
        draw_rounded_rect(self.canvas, 20, y_pos, 20 + w_search, y_pos+45, 22, bg_input)
        
        # Ikon Kaca Pembesar
        ix, iy = 45, y_pos + 22
        self.canvas.create_oval(ix-6, iy-6, ix+6, iy+6, outline="#9E9E9E", width=2)
        self.canvas.create_line(ix+4, iy+4, ix+10, iy+10, fill="#9E9E9E", width=2, capstyle="round")

        # Widget Entry
        entry = tk.Entry(self.canvas.master, textvariable=self.var_search, font=("Arial", 11), bd=0, bg=bg_input, fg=Theme.TEXT)
        entry.place(x=65, y=y_pos+13, width=w_search - 90, height=20)
        self.widgets.append(entry)
        entry.bind("<KeyRelease>", lambda e: self.render_list())

        # Tombol Reset (X)
        btn_reset_x = 20 + w_search - 25
        self.canvas.create_text(btn_reset_x, y_pos+22, text="✕", font=("Arial", 11, "bold"), fill="#BDBDBD", tags="btn_reset")
        self.canvas.tag_bind("btn_reset", "<Button-1>", lambda e: self.reset_search())
        self.efek_hover("btn_reset")

        # 2. TOMBOL FILTER (Menggambar Manual)
        filter_x = self.W - 50
        
        # Gambar Tombol
        tag_filter = "btn_filter_klik"
        draw_rounded_rect(self.canvas, filter_x, y_pos, filter_x+40, y_pos+45, 12, "#E0E0E0", tags=tag_filter) # Shadow
        draw_rounded_rect(self.canvas, filter_x, y_pos, filter_x+40, y_pos+43, 12, Theme.WHITE, tags=tag_filter) # Body
        
        # Ikon Corong
        fx, fy = filter_x + 20, y_pos + 22
        points = [fx-7, fy-5, fx+7, fy-5, fx+2, fy+1, fx+2, fy+6, fx-2, fy+6, fx-2, fy+1]
        self.canvas.create_polygon(points, fill="#555555", outline="", tags=tag_filter)
        
        # Klik Tombol Filter -> Muncul Popup
        self.canvas.tag_bind(tag_filter, "<Button-1>", self.show_filter_popup)
        self.efek_hover(tag_filter)

    def show_filter_popup(self, event):
        """Popup Menu: Hanya 'Semua', 'Pemasukan', 'Pengeluaran'"""
        menu = tk.Menu(self.canvas.master, tearoff=0, bg="white", fg=Theme.TEXT, font=("Arial", 10))
        
        # Opsi disesuaikan permintaan
        options = ["Semua", "Pemasukan", "Pengeluaran"]
        
        for opt in options:
            label = f"✓ {opt}" if self.filter_selected == opt else f"   {opt}"
            menu.add_command(label=label, command=lambda x=opt: self.apply_filter(x))
        
        menu.post(event.x_root, event.y_root)

    def apply_filter(self, selection):
        self.filter_selected = selection
        self.render_list()

    def reset_search(self):
        self.var_search.set("")
        self.render_list()
        self.canvas.focus_set()

    def render_list(self):
        self.canvas.delete("list_item") 
        
        keyword = self.var_search.get().lower()
        kategori = self.filter_selected
        
        y_start = 210
        found_count = 0
        
        # Loop data yang diterima dari backend (bukan dummy local lagi)
        for item in self.data_transaksi:
            # --- LOGIKA FILTER REVISI (Cuma In/Out) ---
            if kategori == "Pemasukan" and item['type'] != "in": continue
            if kategori == "Pengeluaran" and item['type'] != "out": continue
            
            # Cek Search Keyword
            if keyword not in item['title'].lower(): continue
            
            self.draw_item(y_start, item)
            y_start += 85
            found_count += 1
        
        if found_count == 0:
            self.canvas.create_text(self.W/2, 350, text="Tidak ada transaksi", font=Theme.F_BODY, fill="#BDBDBD", tags="list_item")

    def draw_item(self, y, item):
        # Cek tipe cuma IN atau OUT
        if item['type'] == "in":
            color, sign, bg_icon = Theme.INCOME, "+", Theme.BTN_GREEN
        else: # Default ke Pengeluaran (Out)
            color, sign, bg_icon = Theme.EXPENSE, "-", Theme.BTN_RED

        tag = "list_item"
        
        # Gambar Kartu
        draw_rounded_rect(self.canvas, 22, y+3, self.W-18, y+78, 18, "#E0E0E0", tags=tag)
        draw_rounded_rect(self.canvas, 20, y, self.W-20, y+75, 18, Theme.WHITE, tags=tag)
        
        # Ikon & Teks
        self.canvas.create_oval(35, y+15, 80, y+60, fill=bg_icon, outline="", tags=tag)
        self.canvas.create_text(57, y+37, text=item['title'][0], font=("Arial", 15, "bold"), fill=color, tags=tag)

        # Sederhanakan Judul untuk Daftar
        display_title = item['title']
        if "Transfer ke" in display_title and "(" in display_title:
            # Extract name inside (...)
            import re
            match = re.search(r"\((.*?)\)", display_title)
            if match:
                display_title = f"Transfer ke {match.group(1)}"
        
        # Batasi Panjang
        if len(display_title) > 25:
            display_title = display_title[:22] + "..."

        self.canvas.create_text(95, y+25, text=display_title, anchor="w", font=Theme.F_BODY, fill=Theme.TEXT, tags=tag)
        self.canvas.create_text(95, y+50, text=item['date'], anchor="w", font=Theme.F_SMALL, fill="#9E9E9E", tags=tag)
        
        # Nominal (Kanan Atas)
        str_duit = f"{sign} Rp {item['amount']:,}".replace(",", ".")
        self.canvas.create_text(self.W-35, y+25, text=str_duit, anchor="e", font=("Arial", 12, "bold"), fill=color, tags=tag)

        # Tombol Detail (Kanan Bawah)
        btn_w = 60
        btn_h = 24
        btn_x2 = self.W - 35
        btn_x1 = btn_x2 - btn_w
        btn_y1 = y+45
        btn_y2 = btn_y1 + btn_h
        
        draw_rounded_rect(self.canvas, btn_x1, btn_y1, btn_x2, btn_y2, 10, "#E0E0E0", tags=tag) 
        self.canvas.create_text((btn_x1+btn_x2)/2, (btn_y1+btn_y2)/2, text="Detail", font=("Arial", 9, "bold"), fill="#555", tags=tag)

        # Klik ITEM -> Tampilkan Detail
        self.canvas.tag_bind(tag, "<Button-1>", lambda e, x=item: self.show_detail(x))
        self.efek_hover(tag)

    def show_detail(self, item):
        self.clear_screen()
        
        # --- HEADER DETAIL ---
        self.canvas.create_rectangle(0, 0, self.W, 100, fill=Theme.PRIMARY, outline="")
        
        # Back Button (Exact Replica of TopUp)
        btn_back = ctk.CTkButton(self.canvas.master, text="←", font=("Arial", 24, "bold"), 
                                 fg_color=Theme.WHITE, text_color=Theme.PRIMARY,
                                 width=40, height=40, corner_radius=20, 
                                 cursor="hand2", hover_color=Theme.BTN_HOVER_LIGHT,
                                 bg_color=Theme.PRIMARY,
                                 command=self.draw)
        btn_back.place(x=20, y=30)
        self.widgets.append(btn_back)
        
        self.canvas.create_text(self.W/2, 50, text="Detail Transaksi", font=Theme.F_HEAD, fill=Theme.WHITE)
        
        # --- CONTENT ---
        y_start = 130
        
        # 1. Status Indicator (Circle Icon + Text)
        circle_r = 30
        cx, cy = self.W/2, y_start
        self.canvas.create_oval(cx-circle_r, cy-circle_r, cx+circle_r, cy+circle_r, fill=Theme.BTN_GREEN, outline="")
        self.canvas.create_text(cx, cy, text="✓", font=("Arial", 24, "bold"), fill="white")
        
        self.canvas.create_text(cx, cy+45, text="Transaksi Berhasil", font=("Arial", 14, "bold"), fill=Theme.PRIMARY)
        
        # 2. Amount (Hero)
        sign = "+" if item['type'] == "in" else "-"
        color = Theme.INCOME if item['type'] == "in" else Theme.EXPENSE
        amount_str = f"{sign} Rp {item['amount']:,}".replace(",", ".")
        
        self.canvas.create_text(cx, cy+80, text=amount_str, font=("Arial", 28, "bold"), fill=color)
        
        # 3. Info Card
        box_y = cy + 120
        box_h = 240
        box_margin = 30
        card_w = self.W - (box_margin * 2)
        
        # Shadow Effect
        draw_rounded_rect(self.canvas, box_margin+2, box_y+2, box_margin+card_w+2, box_y+box_h+2, 20, "#E0E0E0")
        # Main Card
        draw_rounded_rect(self.canvas, box_margin, box_y, box_margin+card_w, box_y+box_h, 20, Theme.WHITE)
        
        # Labels
        labels = [
            ("Judul", item['title']),
            ("Tanggal", item['date']),
            ("Kategori", "Pemasukan" if item['type'] == 'in' else "Pengeluaran"),
            ("ID Transaksi", f"TRX-{item.get('id', 0):08d}")
        ]
        
        py = box_y + 35
        for i, (lbl, val) in enumerate(labels):
            # Label (Left)
            self.canvas.create_text(box_margin+20, py, text=lbl, anchor="w", font=("Arial", 11), fill="#757575")
            
            # Value (Right) -> Multiline handling if title is too long? For now keep simple right align
            limit = 25
            if len(str(val)) > limit:
                val = str(val)[:limit] + "..."
            
            self.canvas.create_text(box_margin+card_w-20, py, text=str(val), anchor="e", font=("Arial", 12, "bold"), fill=Theme.TEXT)
            
            # Divider (except last item)
            if i < len(labels) - 1:
                line_y = py + 30
                self.canvas.create_line(box_margin+20, line_y, box_margin+card_w-20, line_y, fill="#F5F5F5", width=1)
            
            py += 60
            
    def draw_bottom_nav(self):
        y_bg = self.H - 90
        self.canvas.create_rectangle(0, y_bg, self.W, self.H, fill=Theme.WHITE, outline="#EEEEEE")
        
        items = [("Home","home","home"), ("Riwayat","history",None)]
        cw = self.W / 2; y_icon = self.H - 55
        
        for i, (lbl, icon, target) in enumerate(items):
            x = (i * cw) + (cw / 2)
            is_active = (icon == "history")
            color = Theme.PRIMARY if is_active else "#CFD8DC"
            tag = f"nav_{lbl}"
            
            draw_nav_icon(self.canvas, x, y_icon, icon, color, tag=tag)
            font_nav = ("Arial", 10, "bold") if is_active else Theme.F_SMALL
            self.canvas.create_text(x, y_icon+30, text=lbl, font=font_nav, fill=color, tags=tag)
            
            if target:
                self.canvas.tag_bind(tag, "<Button-1>", lambda e, t=target: self.safe_navigate(t))
                self.efek_hover(tag)

    def safe_navigate(self, target):
        self.clear_screen()
        self.navigate(target)

    def clear_screen(self):
        self.canvas.delete("all")
        for w in self.widgets:
            w.destroy()
        self.widgets = []

    def efek_hover(self, tag):
        self.canvas.tag_bind(tag, "<Enter>", lambda e: self.canvas.config(cursor="hand2"))
        self.canvas.tag_bind(tag, "<Leave>", lambda e: self.canvas.config(cursor=""))