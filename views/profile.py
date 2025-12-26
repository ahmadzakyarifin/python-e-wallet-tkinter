import customtkinter as ctk
from tkinter import messagebox
import os


class ProfileApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Konfigurasi window
        self.title("DANA Profile")
        self.geometry("400x700")
        self.resizable(False, False)

        # Set tema
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("green")

        # Data user (simulasi)
        self.user_data = {
            "nama": "Ahmad Rizki",
            "no_hp": "+62 812-3456-7890",
            "email": "ahmad.rizki@email.com",
            "saldo": 1250000,
            "level": "Premium",
            "poin": 2500,
        }

        self.create_widgets()

    def create_widgets(self):
        # Main container dengan scrollbar
        main_frame = ctk.CTkScrollableFrame(self, fg_color="#F8F9FA")
        main_frame.pack(fill="both", expand=True)

        # Header dengan foto profil
        header_frame = ctk.CTkFrame(main_frame, fg_color="#00D26A", corner_radius=0)
        header_frame.pack(fill="x", pady=(0, 20))

        # Foto profil (simulasi dengan lingkaran)
        profile_circle = ctk.CTkFrame(
            header_frame, width=100, height=100, fg_color="#FFFFFF", corner_radius=50
        )
        profile_circle.pack(pady=(30, 10))

        initial_label = ctk.CTkLabel(
            profile_circle, text="AR", font=("Arial", 32, "bold"), text_color="#00D26A"
        )
        initial_label.place(relx=0.5, rely=0.5, anchor="center")

        # Nama user
        name_label = ctk.CTkLabel(
            header_frame,
            text=self.user_data["nama"],
            font=("Arial", 20, "bold"),
            text_color="#FFFFFF",
        )
        name_label.pack(pady=(5, 5))

        # Level/Status
        level_label = ctk.CTkLabel(
            header_frame,
            text=f"⭐ {self.user_data['level']} Member",
            font=("Arial", 12),
            text_color="#FFFFFF",
        )
        level_label.pack(pady=(0, 20))

        # Card Saldo
        saldo_card = ctk.CTkFrame(
            main_frame,
            fg_color="#FFFFFF",
            corner_radius=15,
            border_width=1,
            border_color="#E0E0E0",
        )
        saldo_card.pack(fill="x", padx=20, pady=(0, 20))

        saldo_header = ctk.CTkLabel(
            saldo_card, text="💰 Saldo DANA", font=("Arial", 14), text_color="#666666"
        )
        saldo_header.pack(pady=(15, 5), anchor="w", padx=20)

        saldo_value = ctk.CTkLabel(
            saldo_card,
            text=f"Rp {self.user_data['saldo']:,.0f}".replace(",", "."),
            font=("Arial", 28, "bold"),
            text_color="#00D26A",
        )
        saldo_value.pack(pady=(0, 15), anchor="w", padx=20)

        # Poin DANA
        poin_card = ctk.CTkFrame(main_frame, fg_color="#FFF3E0", corner_radius=15)
        poin_card.pack(fill="x", padx=20, pady=(0, 20))

        poin_content = ctk.CTkFrame(poin_card, fg_color="transparent")
        poin_content.pack(fill="x", padx=20, pady=15)

        poin_left = ctk.CTkFrame(poin_content, fg_color="transparent")
        poin_left.pack(side="left")

        ctk.CTkLabel(
            poin_left, text="🎯 Poin DANA", font=("Arial", 14), text_color="#F57C00"
        ).pack(anchor="w")

        ctk.CTkLabel(
            poin_left,
            text=f"{self.user_data['poin']:,} Poin",
            font=("Arial", 18, "bold"),
            text_color="#F57C00",
        ).pack(anchor="w")

        # Informasi Akun
        info_label = ctk.CTkLabel(
            main_frame,
            text="Informasi Akun",
            font=("Arial", 16, "bold"),
            text_color="#333333",
        )
        info_label.pack(anchor="w", padx=20, pady=(10, 10))

        # Menu items
        menu_items = [
            ("📱", "Nomor Telepon", self.user_data["no_hp"]),
            ("📧", "Email", self.user_data["email"]),
            ("🆔", "User ID", "DANA123456789"),
            ("🔒", "Keamanan", "PIN & Biometrik Aktif"),
        ]

        for icon, title, value in menu_items:
            self.create_menu_item(main_frame, icon, title, value)

        # Pengaturan
        settings_label = ctk.CTkLabel(
            main_frame,
            text="Pengaturan",
            font=("Arial", 16, "bold"),
            text_color="#333333",
        )
        settings_label.pack(anchor="w", padx=20, pady=(20, 10))

        # Tombol pengaturan
        settings_buttons = [
            ("🔔", "Notifikasi"),
            ("🌐", "Bahasa", "Indonesia"),
            ("🎨", "Tema Aplikasi", "Terang"),
            ("❓", "Bantuan & Pusat Informasi"),
            ("📄", "Syarat & Ketentuan"),
            ("🔐", "Privasi"),
        ]

        for item in settings_buttons:
            if len(item) == 2:
                icon, title = item
                value = None
            else:
                icon, title, value = item
            self.create_menu_item(main_frame, icon, title, value, clickable=True)

        # Tombol Logout
        logout_btn = ctk.CTkButton(
            main_frame,
            text="Keluar dari Akun",
            font=("Arial", 14, "bold"),
            fg_color="#FF3B30",
            hover_color="#CC2E26",
            height=45,
            corner_radius=10,
            command=self.logout,
        )
        logout_btn.pack(fill="x", padx=20, pady=(30, 20))

        # Versi aplikasi
        version_label = ctk.CTkLabel(
            main_frame, text="Versi 4.78.0", font=("Arial", 10), text_color="#999999"
        )
        version_label.pack(pady=(10, 30))

    def create_menu_item(self, parent, icon, title, value=None, clickable=False):
        item_frame = ctk.CTkFrame(
            parent,
            fg_color="#FFFFFF",
            corner_radius=10,
            border_width=1,
            border_color="#E0E0E0",
        )
        item_frame.pack(fill="x", padx=20, pady=(0, 8))

        if clickable:
            item_frame.bind("<Button-1>", lambda e: self.on_menu_click(title))

        content_frame = ctk.CTkFrame(item_frame, fg_color="transparent")
        content_frame.pack(fill="x", padx=15, pady=12)

        # Icon dan title
        left_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        left_frame.pack(side="left", fill="x", expand=True)

        icon_label = ctk.CTkLabel(left_frame, text=icon, font=("Arial", 20))
        icon_label.pack(side="left", padx=(0, 10))

        text_frame = ctk.CTkFrame(left_frame, fg_color="transparent")
        text_frame.pack(side="left", fill="x", expand=True)

        title_label = ctk.CTkLabel(
            text_frame, text=title, font=("Arial", 13), text_color="#333333"
        )
        title_label.pack(anchor="w")

        if value:
            value_label = ctk.CTkLabel(
                text_frame, text=value, font=("Arial", 11), text_color="#999999"
            )
            value_label.pack(anchor="w")

        # Arrow untuk clickable items
        if clickable or value:
            arrow_label = ctk.CTkLabel(
                content_frame, text="›", font=("Arial", 24), text_color="#CCCCCC"
            )
            arrow_label.pack(side="right")

    def on_menu_click(self, menu_name):
        messagebox.showinfo("Info", f"Membuka: {menu_name}")

    def logout(self):
        response = messagebox.askyesno("Konfirmasi", "Apakah Anda yakin ingin keluar?")
        if response:
            messagebox.showinfo("Info", "Berhasil keluar dari akun")
            self.quit()


if __name__ == "__main__":
    app = ProfileApp()
    app.mainloop()
