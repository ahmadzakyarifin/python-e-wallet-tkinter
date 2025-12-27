import customtkinter as ctk
from tkinter import messagebox


class SettingsApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Konfigurasi window
        self.title("E-SAKU - Settings")
        self.geometry("400x700")
        self.resizable(False, False)

        # Set tema
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("green")

        # Data pengaturan
        self.settings_data = {
            "notifikasi": True,
            "biometrik": True,
            "tema_gelap": False,
            "bahasa": "Indonesia",
        }

        self.create_widgets()

    def create_widgets(self):
        # Main container dengan scrollbar
        main_frame = ctk.CTkScrollableFrame(self, fg_color="#F8F9FA")
        main_frame.pack(fill="both", expand=True)

        # Header
        header_frame = ctk.CTkFrame(
            main_frame, fg_color="#00D26A", corner_radius=0, height=100
        )
        header_frame.pack(fill="x", pady=(0, 20))
        header_frame.pack_propagate(False)

        # Tombol kembali dan judul
        header_content = ctk.CTkFrame(header_frame, fg_color="transparent")
        header_content.pack(fill="both", expand=True, padx=20, pady=20)

        back_button = ctk.CTkButton(
            header_content,
            text="←",
            font=("Arial", 24),
            width=40,
            height=40,
            fg_color="transparent",
            hover_color="#00B85C",
            command=self.go_back,
        )
        back_button.pack(side="left")

        title_label = ctk.CTkLabel(
            header_content,
            text="Pengaturan",
            font=("Arial", 24, "bold"),
            text_color="#FFFFFF",
        )
        title_label.pack(side="left", padx=20)

        # Akun & Keamanan
        self.create_section_title(main_frame, "🔐 Akun & Keamanan")

        security_items = [
            ("Ubah PIN", "6 digit"),
            ("Ubah Password", "••••••••"),
            ("Verifikasi Akun", "Email & Nomor HP"),
        ]

        for title, value in security_items:
            self.create_menu_item(main_frame, title, value)

        # Toggle Biometrik
        self.create_toggle_item(
            main_frame,
            "Autentikasi Biometrik",
            "biometrik",
            "Gunakan sidik jari atau wajah",
        )

        # Notifikasi
        self.create_section_title(main_frame, "🔔 Notifikasi")

        self.create_toggle_item(
            main_frame,
            "Notifikasi Push",
            "notifikasi",
            "Terima pemberitahuan transaksi",
        )

        # Tampilan
        self.create_section_title(main_frame, "🎨 Tampilan")

        self.create_toggle_item(
            main_frame, "Mode Gelap", "tema_gelap", "Ubah tema aplikasi"
        )

        display_items = [
            ("Bahasa", self.settings_data["bahasa"]),
            ("Ukuran Font", "Sedang"),
        ]

        for title, value in display_items:
            self.create_menu_item(main_frame, title, value)

        # Privasi
        self.create_section_title(main_frame, "🔒 Privasi")

        privacy_items = [
            ("Riwayat Transaksi", "Kelola data transaksi"),
            ("Hapus Cache", "234 MB"),
        ]

        for title, value in privacy_items:
            self.create_menu_item(main_frame, title, value)

        # Bantuan
        self.create_section_title(main_frame, "❓ Bantuan & Dukungan")

        help_items = [
            ("Pusat Bantuan", "FAQ & Panduan"),
            ("Hubungi Kami", "Customer Service 24/7"),
        ]

        for title, value in help_items:
            self.create_menu_item(main_frame, title, value)

        # Tentang
        self.create_section_title(main_frame, "ℹ️ Tentang")

        about_items = [
            ("Versi Aplikasi", "4.78.0"),
            ("Syarat & Ketentuan", "Baca S&K"),
            ("Kebijakan Privasi", "Baca kebijakan"),
        ]

        for title, value in about_items:
            self.create_menu_item(main_frame, title, value)

        # Tombol Logout
        logout_btn = ctk.CTkButton(
            main_frame,
            text="🚪 Keluar dari Akun",
            font=("Arial", 14, "bold"),
            fg_color="#FF3B30",
            hover_color="#CC2E26",
            height=50,
            corner_radius=12,
            command=self.logout,
        )
        logout_btn.pack(fill="x", padx=20, pady=(30, 10))

        # Hapus Akun
        delete_btn = ctk.CTkButton(
            main_frame,
            text="Hapus Akun",
            font=("Arial", 12),
            fg_color="transparent",
            text_color="#FF3B30",
            hover_color="#FFE5E5",
            height=40,
            command=self.delete_account,
        )
        delete_btn.pack(fill="x", padx=20, pady=(0, 40))

    def create_section_title(self, parent, title):
        title_frame = ctk.CTkFrame(parent, fg_color="transparent")
        title_frame.pack(fill="x", padx=20, pady=(20, 10))

        label = ctk.CTkLabel(
            title_frame,
            text=title,
            font=("Arial", 16, "bold"),
            text_color="#333333",
            anchor="w",
        )
        label.pack(fill="x")

    def create_menu_item(self, parent, title, value):
        item_frame = ctk.CTkFrame(
            parent,
            fg_color="#FFFFFF",
            corner_radius=12,
            border_width=1,
            border_color="#E0E0E0",
            cursor="hand2",
        )
        item_frame.pack(fill="x", padx=20, pady=(0, 8))

        # Bind click event
        item_frame.bind("<Button-1>", lambda e: self.on_menu_click(title))

        content_frame = ctk.CTkFrame(item_frame, fg_color="transparent")
        content_frame.pack(fill="x", padx=15, pady=12)
        content_frame.bind("<Button-1>", lambda e: self.on_menu_click(title))

        # Left side
        left_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        left_frame.pack(side="left", fill="both", expand=True)
        left_frame.bind("<Button-1>", lambda e: self.on_menu_click(title))

        title_label = ctk.CTkLabel(
            left_frame,
            text=title,
            font=("Arial", 13, "bold"),
            text_color="#333333",
            anchor="w",
        )
        title_label.pack(anchor="w", fill="x")
        title_label.bind("<Button-1>", lambda e: self.on_menu_click(title))

        value_label = ctk.CTkLabel(
            left_frame, text=value, font=("Arial", 11), text_color="#999999", anchor="w"
        )
        value_label.pack(anchor="w", fill="x")
        value_label.bind("<Button-1>", lambda e: self.on_menu_click(title))

        # Arrow
        arrow_label = ctk.CTkLabel(
            content_frame, text="›", font=("Arial", 24), text_color="#CCCCCC"
        )
        arrow_label.pack(side="right")
        arrow_label.bind("<Button-1>", lambda e: self.on_menu_click(title))

    def create_toggle_item(self, parent, title, setting_key, description):
        item_frame = ctk.CTkFrame(
            parent,
            fg_color="#FFFFFF",
            corner_radius=12,
            border_width=1,
            border_color="#E0E0E0",
        )
        item_frame.pack(fill="x", padx=20, pady=(0, 8))

        content_frame = ctk.CTkFrame(item_frame, fg_color="transparent")
        content_frame.pack(fill="x", padx=15, pady=12)

        # Left side
        left_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        left_frame.pack(side="left", fill="both", expand=True)

        title_label = ctk.CTkLabel(
            left_frame,
            text=title,
            font=("Arial", 13, "bold"),
            text_color="#333333",
            anchor="w",
        )
        title_label.pack(anchor="w", fill="x")

        desc_label = ctk.CTkLabel(
            left_frame,
            text=description,
            font=("Arial", 11),
            text_color="#999999",
            anchor="w",
        )
        desc_label.pack(anchor="w", fill="x")

        # Switch toggle
        switch = ctk.CTkSwitch(
            content_frame,
            text="",
            width=50,
            fg_color="#CCCCCC",
            progress_color="#00D26A",
            button_color="#FFFFFF",
            button_hover_color="#F0F0F0",
            command=lambda: self.toggle_setting(setting_key, switch),
        )
        switch.pack(side="right")

        # Set nilai awal
        if self.settings_data.get(setting_key, False):
            switch.select()

    def toggle_setting(self, key, switch):
        self.settings_data[key] = switch.get() == 1
        status = "diaktifkan" if self.settings_data[key] else "dinonaktifkan"

        # Khusus untuk tema gelap
        if key == "tema_gelap":
            mode = "dark" if self.settings_data[key] else "light"
            ctk.set_appearance_mode(mode)
            messagebox.showinfo("Info", f"Mode gelap {status}")
        else:
            messagebox.showinfo("Info", f"{key.capitalize()} {status}")

    def on_menu_click(self, menu_name):
        if menu_name == "Bahasa":
            self.show_language_dialog()
        elif menu_name == "Hapus Cache":
            self.clear_cache()
        else:
            messagebox.showinfo("Info", f"Membuka: {menu_name}")

    def show_language_dialog(self):
        dialog = ctk.CTkToplevel(self)
        dialog.title("Pilih Bahasa")
        dialog.geometry("300x250")
        dialog.resizable(False, False)
        dialog.grab_set()

        ctk.CTkLabel(dialog, text="Pilih Bahasa", font=("Arial", 16, "bold")).pack(
            pady=20
        )

        languages = ["Indonesia", "English", "Melayu"]

        for lang in languages:
            btn = ctk.CTkButton(
                dialog,
                text=lang,
                height=40,
                fg_color=(
                    "#00D26A" if lang == self.settings_data["bahasa"] else "#F0F0F0"
                ),
                text_color=(
                    "#FFFFFF" if lang == self.settings_data["bahasa"] else "#333333"
                ),
                hover_color="#00B85C",
                command=lambda l=lang: self.set_language(l, dialog),
            )
            btn.pack(fill="x", padx=20, pady=5)

    def set_language(self, lang, dialog):
        self.settings_data["bahasa"] = lang
        dialog.destroy()
        messagebox.showinfo("Berhasil", f"Bahasa diubah ke {lang}")

    def clear_cache(self):
        response = messagebox.askyesno("Konfirmasi", "Hapus cache aplikasi (234 MB)?")
        if response:
            messagebox.showinfo("Berhasil", "Cache berhasil dihapus!")

    def go_back(self):
        messagebox.showinfo("Info", "Kembali ke halaman sebelumnya")

    def logout(self):
        response = messagebox.askyesno(
            "Konfirmasi", "Apakah Anda yakin ingin keluar dari akun?"
        )
        if response:
            messagebox.showinfo("Berhasil", "Anda telah keluar dari akun")
            self.quit()

    def delete_account(self):
        response = messagebox.askyesno(
            "Peringatan",
            "Apakah Anda yakin ingin menghapus akun?\n\n"
            "Tindakan ini tidak dapat dibatalkan!",
            icon="warning",
        )
        if response:
            messagebox.showinfo("Berhasil", "Akun telah dihapus")
            self.quit()


if __name__ == "__main__":
    app = SettingsApp()
    app.mainloop()
