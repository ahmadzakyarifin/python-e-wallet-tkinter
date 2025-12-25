import customtkinter as ctk
import tkinter.messagebox as msgbox
import platform

# ==========================================
# BAGIAN 1: KONFIGURASI TEMA & OS
# ==========================================

os_name = platform.system()
if os_name == "Windows":
    FONT_FAMILY = "Segoe UI"
    try:
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
    except:
        pass
else:
    FONT_FAMILY = "DejaVu Sans"

class Theme:
    PRIMARY   = "#00C853"  # Hijau Utama
    BG        = "#F0F2F5"  # Background Window
    WHITE     = "#FFFFFF"
    TEXT      = "#2D3436"  
    MUTED     = "#636E72"  
    INPUT_BG  = "#E8F5E9"  
    HOVER_BTN = "#00E676"  
    
    F_HEAD    = (FONT_FAMILY, 30, "bold") 
    F_SUB     = (FONT_FAMILY, 16)         
    F_TITLE   = (FONT_FAMILY, 11, "bold") 
    F_BODY    = (FONT_FAMILY, 12)         
    F_BTN     = (FONT_FAMILY, 13, "bold")

# ==========================================
# BAGIAN 2: APLIKASI UTAMA
# ==========================================

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("green") 

class ESakuApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.W, self.H = 520, 930 
        self.geometry(f"{self.W}x{self.H}")
        self.title("E-SAKU - Solusi Saku Digital") 
        self.resizable(False, False)

        self.main_container = ctk.CTkFrame(self, fg_color=Theme.BG)
        self.main_container.pack(fill="both", expand=True)

        self.show_welcome_page()

    def clear_frame(self):
        for widget in self.main_container.winfo_children():
            widget.destroy()

    # --- HELPER UI ---
    def create_back_button(self, parent):
        btn = ctk.CTkButton(
            parent, text="←", width=45, height=45, corner_radius=22.5,         
            fg_color=Theme.WHITE, text_color=Theme.PRIMARY, hover_color="#FAFAFA",
            font=(FONT_FAMILY, 24, "bold"), command=self.show_welcome_page
        )
        btn.place(x=25, y=25) 

    def create_header_bg(self, height):
        header = ctk.CTkFrame(self.main_container, fg_color=Theme.PRIMARY, height=height, corner_radius=0)
        header.pack(fill="x", side="top")
        
        # PERBAIKAN BUG HIASAN REGISTER
        # Posisi digeser sedikit ke atas dan kanan (x=340, y=-100) agar tidak terpotong kartu putih
        ctk.CTkLabel(header, text="", width=250, height=250, fg_color="#00E676", corner_radius=125).place(x=340, y=-100)
        return header

    # ================= PAGE 1: WELCOME SCREEN =================
    def show_welcome_page(self):
        self.clear_frame()
        
        bg = ctk.CTkFrame(self.main_container, fg_color=Theme.PRIMARY, corner_radius=0)
        bg.pack(fill="both", expand=True)

        ctk.CTkLabel(bg, text="", width=300, height=300, fg_color="#00E676", corner_radius=150).place(x=-100, y=-50)

        center_frame = ctk.CTkFrame(bg, fg_color="transparent")
        center_frame.place(relx=0.5, rely=0.4, anchor="center")

        ctk.CTkLabel(center_frame, text="E-SAKU", font=(FONT_FAMILY, 48, "bold"), text_color="white").pack()
        ctk.CTkLabel(center_frame, text="Solusi Saku Digital", font=Theme.F_SUB, text_color="#E8F5E9").pack(pady=5)

        bottom_frame = ctk.CTkFrame(bg, fg_color="transparent")
        bottom_frame.place(relx=0.5, rely=0.85, anchor="center", relwidth=1)

        ctk.CTkButton(
            bottom_frame, text="Masuk Akun",
            fg_color=Theme.WHITE, text_color=Theme.PRIMARY,
            hover_color="#F1F8E9", height=55, corner_radius=27,
            font=Theme.F_BTN, command=self.show_login_page
        ).pack(pady=10, ipadx=30)

        ctk.CTkButton(
            bottom_frame, text="Buka Rekening Baru",
            fg_color="transparent", text_color=Theme.WHITE,
            border_width=2, border_color=Theme.WHITE,
            hover_color=Theme.HOVER_BTN, height=55, corner_radius=27,
            font=Theme.F_BTN, command=self.show_register_page
        ).pack(pady=5, ipadx=10)
        
        ctk.CTkLabel(bg, text="v1.4 (Final UI Fix)", font=(FONT_FAMILY, 10), text_color="#C8E6C9").place(relx=0.5, rely=0.97, anchor="center")

    # ================= PAGE 2: LOGIN (PERBAIKAN) =================
    def show_login_page(self):
        self.clear_frame()

        header = self.create_header_bg(height=320)
        self.create_back_button(header)
        
        # PERBAIKAN 2: Teks Header Bahasa Indonesia
        ctk.CTkLabel(
            header, text="Selamat Datang di\nE-SAKU", 
            font=Theme.F_HEAD, text_color="white", justify="center"
        ).place(relx=0.5, rely=0.45, anchor="center")

        card = ctk.CTkFrame(self.main_container, fg_color=Theme.WHITE, corner_radius=30)
        card.place(relx=0.5, rely=0.6, anchor="center", relwidth=0.9, relheight=0.55) 

        content = ctk.CTkFrame(card, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=30, pady=30)

        # Input Form (Label otomatis rata kiri berkat update fungsi create_label di bawah)
        self.create_label(content, "ID Pengguna (HP / Email)")
        self.entry_user = self.create_entry(content, "08xx / nama@email.com")

        self.create_label(content, "Password / PIN", pady=20) 
        self.entry_pass = self.create_entry(content, "********", show="*")

        ctk.CTkButton(content, text="Lupa Password?", fg_color="transparent", text_color=Theme.PRIMARY, font=Theme.F_TITLE, hover=False, width=0, anchor="e").pack(fill="x", pady=(5, 20))

        ctk.CTkButton(
            content, text="LOGIN SEKARANG", fg_color=Theme.PRIMARY, hover_color=Theme.HOVER_BTN,
            height=55, corner_radius=27, font=Theme.F_BTN,
            command=self.dummy_login_action
        ).pack(fill="x")

        footer = ctk.CTkFrame(content, fg_color="transparent")
        footer.pack(side="bottom", pady=15)
        ctk.CTkLabel(footer, text="Belum punya akun?", font=Theme.F_BODY, text_color="gray").pack(side="left")
        ctk.CTkButton(footer, text="Daftar", fg_color="transparent", text_color=Theme.PRIMARY, font=Theme.F_TITLE, hover=False, width=30, command=self.show_register_page).pack(side="left", padx=5)

    # ================= PAGE 3: REGISTER =================
    def show_register_page(self):
        self.clear_frame()

        header = self.create_header_bg(height=250)
        self.create_back_button(header)
        
        ctk.CTkLabel(
            header, text="Registrasi E-SAKU", 
            font=Theme.F_HEAD, text_color="white"
        ).place(relx=0.5, rely=0.4, anchor="center")

        card = ctk.CTkFrame(self.main_container, fg_color=Theme.WHITE, corner_radius=30)
        card.place(relx=0.5, rely=0.6, anchor="center", relwidth=0.9, relheight=0.72)

        content = ctk.CTkFrame(card, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=25, pady=25)

        # Helper Input khusus Register (Agar label rata kiri)
        def add_input(label, placeholder, is_pass=False):
            # Penambahan anchor="w" di sini agar rata kiri
            ctk.CTkLabel(content, text=label, font=Theme.F_TITLE, text_color=Theme.MUTED, anchor="w").pack(fill="x", pady=(8, 0))
            entry = ctk.CTkEntry(
                content, placeholder_text=placeholder,
                font=Theme.F_BODY, text_color=Theme.TEXT,
                fg_color=Theme.INPUT_BG, border_width=0, corner_radius=10,
                height=42, show="*" if is_pass else ""
            )
            entry.pack(fill="x", pady=(2, 0))
            return entry

        self.reg_nama = add_input("Nama Lengkap", "Sesuai KTP")
        self.reg_hp = add_input("No. WhatsApp", "08xxxxxxxxxx")
        self.reg_email = add_input("Email", "email@domain.com")
        self.reg_pass1 = add_input("Password", "Min. 8 karakter", True)

        self.check_var = ctk.StringVar(value="off")
        ctk.CTkCheckBox(
            content, text="Saya setuju dengan S&K E-SAKU",
            variable=self.check_var, onvalue="on", offvalue="off",
            font=Theme.F_TITLE, text_color="gray", fg_color=Theme.PRIMARY,
            border_width=2, checkbox_width=20, checkbox_height=20
        ).pack(fill="x", pady=(20, 10))

        ctk.CTkButton(
            content, text="BUAT AKUN", fg_color=Theme.PRIMARY, hover_color=Theme.HOVER_BTN,
            height=55, corner_radius=27, font=Theme.F_BTN,
            command=self.dummy_register_action
        ).pack(fill="x", side="bottom", pady=10)

    # ================= LOGIC HELPER =================
    def create_label(self, parent, text, pady=5):
        # PERBAIKAN 1: Penambahan anchor="w" langsung di dalam CTkLabel
        # Ini memastikan teks selalu rata kiri meskipun fill="x"
        ctk.CTkLabel(parent, text=text, font=Theme.F_TITLE, text_color=Theme.MUTED, anchor="w").pack(fill="x", pady=(pady, 0))

    def create_entry(self, parent, placeholder, show=""):
        entry = ctk.CTkEntry(
            parent, placeholder_text=placeholder,
            font=Theme.F_BODY, text_color=Theme.TEXT,
            fg_color=Theme.INPUT_BG, border_width=0, corner_radius=10,
            height=45, show=show
        )
        entry.pack(fill="x", pady=(5, 0))
        return entry

    def dummy_login_action(self):
        user = self.entry_user.get()
        pwd = self.entry_pass.get()
        if not user or not pwd:
            msgbox.showwarning("Gagal Masuk", "Mohon isi ID dan Password!")
        else:
            msgbox.showinfo("Berhasil", f"Selamat datang kembali, {user}!")

    def dummy_register_action(self):
        if not self.reg_nama.get():
            msgbox.showwarning("Data Kurang", "Nama lengkap wajib diisi!")
            return
        if self.check_var.get() == "off":
            msgbox.showwarning("Persetujuan", "Anda harus menyetujui Syarat & Ketentuan.")
            return
        msgbox.showinfo("Sukses", "Akun berhasil dibuat! Silakan login.")
        self.show_login_page()

if __name__ == "__main__":
    app = ESakuApp()
    app.mainloop()