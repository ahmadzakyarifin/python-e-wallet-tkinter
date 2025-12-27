import customtkinter as ctk
from tkinter import messagebox
import random
import string


class WithdrawApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Konfigurasi window
        self.title("E-SAKU - Tarik Tunai")
        self.geometry("400x700")
        self.resizable(False, False)

        # Set tema
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("green")

        # Data user
        self.saldo = 1250000
        self.biaya_admin = 2500

        self.create_widgets()

    def create_widgets(self):
        # Main container
        main_frame = ctk.CTkScrollableFrame(self, fg_color="#F8F9FA")
        main_frame.pack(fill="both", expand=True)

        # Header
        header_frame = ctk.CTkFrame(
            main_frame, fg_color="#00D26A", corner_radius=0, height=120
        )
        header_frame.pack(fill="x", pady=(0, 20))
        header_frame.pack_propagate(False)

        # Header content
        header_content = ctk.CTkFrame(header_frame, fg_color="transparent")
        header_content.pack(fill="both", expand=True, padx=20, pady=20)

        # Tombol kembali
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

        # Title
        title_frame = ctk.CTkFrame(header_content, fg_color="transparent")
        title_frame.pack(side="left", padx=20, fill="both", expand=True)

        title_label = ctk.CTkLabel(
            title_frame,
            text="Tarik Tunai",
            font=("Arial", 24, "bold"),
            text_color="#FFFFFF",
            anchor="w",
        )
        title_label.pack(anchor="w")

        # Saldo
        saldo_label = ctk.CTkLabel(
            title_frame,
            text=f"Saldo: Rp {self.saldo:,}".replace(",", "."),
            font=("Arial", 12),
            text_color="#FFFFFF",
            anchor="w",
        )
        saldo_label.pack(anchor="w")

        # Info Card
        info_frame = ctk.CTkFrame(
            main_frame,
            fg_color="#E3F2FD",
            corner_radius=12,
            border_width=1,
            border_color="#90CAF9",
        )
        info_frame.pack(fill="x", padx=20, pady=(0, 20))

        info_content = ctk.CTkFrame(info_frame, fg_color="transparent")
        info_content.pack(fill="x", padx=15, pady=12)

        info_icon = ctk.CTkLabel(info_content, text="ℹ️", font=("Arial", 20))
        info_icon.pack(side="left", padx=(0, 10))

        info_text = ctk.CTkLabel(
            info_content,
            text="Tarik tunai tanpa kartu di ATM\nBCA, BNI, BRI, Mandiri, & Indomaret",
            font=("Arial", 11),
            text_color="#1976D2",
            anchor="w",
            justify="left",
        )
        info_text.pack(side="left", fill="x", expand=True)

        # Form Container
        form_frame = ctk.CTkFrame(
            main_frame,
            fg_color="#FFFFFF",
            corner_radius=15,
            border_width=1,
            border_color="#E0E0E0",
        )
        form_frame.pack(fill="x", padx=20, pady=(0, 20))

        form_content = ctk.CTkFrame(form_frame, fg_color="transparent")
        form_content.pack(fill="x", padx=20, pady=20)

        # Input Nominal
        nominal_label = ctk.CTkLabel(
            form_content,
            text="Nominal Penarikan",
            font=("Arial", 13, "bold"),
            text_color="#333333",
            anchor="w",
        )
        nominal_label.pack(fill="x", pady=(0, 5))

        # Frame untuk input nominal dengan prefix Rp
        nominal_frame = ctk.CTkFrame(
            form_content,
            fg_color="#F8F9FA",
            corner_radius=8,
            border_width=1,
            border_color="#E0E0E0",
            height=45,
        )
        nominal_frame.pack(fill="x", pady=(0, 10))
        nominal_frame.pack_propagate(False)

        rp_label = ctk.CTkLabel(
            nominal_frame, text="Rp", font=("Arial", 14), text_color="#666666"
        )
        rp_label.pack(side="left", padx=(15, 5))

        self.nominal_entry = ctk.CTkEntry(
            nominal_frame,
            placeholder_text="0",
            font=("Arial", 14),
            border_width=0,
            fg_color="transparent",
        )
        self.nominal_entry.pack(side="left", fill="both", expand=True, padx=(0, 15))
        self.nominal_entry.bind("<KeyRelease>", self.format_nominal)

        # Nominal cepat
        quick_frame = ctk.CTkFrame(form_content, fg_color="transparent")
        quick_frame.pack(fill="x", pady=(5, 15))

        quick_amounts = [100000, 200000, 500000, 1000000]
        for i, amount in enumerate(quick_amounts):
            label = f"{amount//1000}K" if amount < 1000000 else "1Jt"
            btn = ctk.CTkButton(
                quick_frame,
                text=label,
                width=80,
                height=35,
                font=("Arial", 12),
                fg_color="#E8F5E9",
                text_color="#00D26A",
                hover_color="#C8E6C9",
                border_width=1,
                border_color="#00D26A",
                command=lambda a=amount: self.set_nominal(a),
            )
            btn.pack(side="left", padx=(0, 8) if i < 3 else 0, expand=True, fill="x")

        # Pilih Lokasi
        lokasi_label = ctk.CTkLabel(
            form_content,
            text="Lokasi Penarikan",
            font=("Arial", 13, "bold"),
            text_color="#333333",
            anchor="w",
        )
        lokasi_label.pack(fill="x", pady=(0, 5))

        self.lokasi_var = ctk.StringVar(value="ATM BCA")

        lokasi_options = ["ATM BCA", "ATM BNI", "ATM BRI", "ATM Mandiri", "Indomaret"]
        self.lokasi_menu = ctk.CTkOptionMenu(
            form_content,
            values=lokasi_options,
            variable=self.lokasi_var,
            height=45,
            font=("Arial", 13),
            fg_color="#F8F9FA",
            button_color="#00D26A",
            button_hover_color="#00B85C",
            dropdown_fg_color="#FFFFFF",
        )
        self.lokasi_menu.pack(fill="x", pady=(0, 15))

        # Biaya Admin Info
        biaya_frame = ctk.CTkFrame(form_content, fg_color="#FFF3E0", corner_radius=8)
        biaya_frame.pack(fill="x", pady=(0, 10))

        biaya_content = ctk.CTkFrame(biaya_frame, fg_color="transparent")
        biaya_content.pack(fill="x", padx=12, pady=10)

        ctk.CTkLabel(biaya_content, text="💰", font=("Arial", 16)).pack(
            side="left", padx=(0, 8)
        )

        biaya_left = ctk.CTkFrame(biaya_content, fg_color="transparent")
        biaya_left.pack(side="left", fill="x", expand=True)

        ctk.CTkLabel(
            biaya_left,
            text="Biaya Admin",
            font=("Arial", 11),
            text_color="#F57C00",
            anchor="w",
        ).pack(anchor="w", fill="x")

        ctk.CTkLabel(
            biaya_content,
            text=f"Rp {self.biaya_admin:,}".replace(",", "."),
            font=("Arial", 13, "bold"),
            text_color="#F57C00",
        ).pack(side="right")

        # Riwayat Penarikan
        history_label = ctk.CTkLabel(
            main_frame,
            text="Riwayat Penarikan",
            font=("Arial", 16, "bold"),
            text_color="#333333",
            anchor="w",
        )
        history_label.pack(fill="x", padx=20, pady=(10, 10))

        # Data riwayat dummy
        recent_withdrawals = [
            {
                "lokasi": "ATM BCA Mandala",
                "nominal": 500000,
                "tanggal": "25 Des 2024",
                "status": "Berhasil",
            },
            {
                "lokasi": "Indomaret Sudirman",
                "nominal": 200000,
                "tanggal": "20 Des 2024",
                "status": "Berhasil",
            },
            {
                "lokasi": "ATM BNI Pusat",
                "nominal": 300000,
                "tanggal": "15 Des 2024",
                "status": "Berhasil",
            },
        ]

        for withdrawal in recent_withdrawals:
            self.create_history_item(main_frame, withdrawal)

        # Tombol Buat Kode
        withdraw_btn = ctk.CTkButton(
            main_frame,
            text="Buat Kode Penarikan",
            font=("Arial", 15, "bold"),
            fg_color="#00D26A",
            hover_color="#00B85C",
            height=55,
            corner_radius=12,
            command=self.process_withdraw,
        )
        withdraw_btn.pack(fill="x", padx=20, pady=(20, 40))

    def create_history_item(self, parent, data):
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

        # Icon
        icon_frame = ctk.CTkFrame(
            content_frame, width=45, height=45, fg_color="#E8F5E9", corner_radius=25
        )
        icon_frame.pack(side="left", padx=(0, 12))
        icon_frame.pack_propagate(False)

        icon_label = ctk.CTkLabel(icon_frame, text="🏧", font=("Arial", 20))
        icon_label.place(relx=0.5, rely=0.5, anchor="center")

        # Info
        info_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        info_frame.pack(side="left", fill="both", expand=True)

        lokasi_label = ctk.CTkLabel(
            info_frame,
            text=data["lokasi"],
            font=("Arial", 13, "bold"),
            text_color="#333333",
            anchor="w",
        )
        lokasi_label.pack(anchor="w", fill="x")

        detail_label = ctk.CTkLabel(
            info_frame,
            text=f"{data['tanggal']} • {data['status']}",
            font=("Arial", 10),
            text_color="#999999",
            anchor="w",
        )
        detail_label.pack(anchor="w", fill="x")

        # Nominal
        nominal_label = ctk.CTkLabel(
            content_frame,
            text=f"Rp {data['nominal']:,}".replace(",", "."),
            font=("Arial", 13, "bold"),
            text_color="#00D26A",
        )
        nominal_label.pack(side="right")

    def format_nominal(self, event):
        value = self.nominal_entry.get().replace(".", "")
        if value.isdigit():
            formatted = f"{int(value):,}".replace(",", ".")
            self.nominal_entry.delete(0, "end")
            self.nominal_entry.insert(0, formatted)

    def set_nominal(self, amount):
        formatted = f"{amount:,}".replace(",", ".")
        self.nominal_entry.delete(0, "end")
        self.nominal_entry.insert(0, formatted)

    def generate_code(self):
        """Generate kode penarikan 10 digit"""
        return "".join(random.choices(string.digits, k=10))

    def validate_withdraw(self):
        nominal_str = self.nominal_entry.get().replace(".", "")

        # Validasi nominal
        if not nominal_str or not nominal_str.isdigit():
            messagebox.showerror("Error", "Nominal penarikan harus diisi dengan angka!")
            return False

        nominal = int(nominal_str)

        if nominal < 50000:
            messagebox.showerror("Error", "Nominal penarikan minimal Rp 50.000!")
            return False

        if nominal > 5000000:
            messagebox.showerror("Error", "Nominal penarikan maksimal Rp 5.000.000!")
            return False

        total = nominal + self.biaya_admin
        if total > self.saldo:
            messagebox.showerror(
                "Error",
                f"Saldo tidak mencukupi!\n\n"
                f"Nominal: Rp {nominal:,}".replace(",", ".") + "\n"
                f"Biaya Admin: Rp {self.biaya_admin:,}".replace(",", ".") + "\n"
                f"Total: Rp {total:,}".replace(",", ".") + "\n"
                f"Saldo Anda: Rp {self.saldo:,}".replace(",", "."),
            )
            return False

        return nominal

    def process_withdraw(self):
        nominal = self.validate_withdraw()
        if not nominal:
            return

        lokasi = self.lokasi_var.get()
        total = nominal + self.biaya_admin

        # Konfirmasi
        message = f"Tarik Tunai\n\n"
        message += f"Lokasi: {lokasi}\n"
        message += f"Nominal: Rp {nominal:,}".replace(",", ".") + "\n"
        message += f"Biaya Admin: Rp {self.biaya_admin:,}".replace(",", ".") + "\n"
        message += f"Total: Rp {total:,}".replace(",", ".") + "\n\n"
        message += "Lanjutkan pembuatan kode penarikan?"

        response = messagebox.askyesno("Konfirmasi Penarikan", message)

        if response:
            # Generate kode
            kode = self.generate_code()

            # Kurangi saldo
            self.saldo -= total

            # Show kode penarikan
            self.show_withdrawal_code(kode, nominal, lokasi, total)

    def show_withdrawal_code(self, kode, nominal, lokasi, total):
        """Dialog untuk menampilkan kode penarikan"""
        dialog = ctk.CTkToplevel(self)
        dialog.title("Kode Penarikan")
        dialog.geometry("350x450")
        dialog.resizable(False, False)
        dialog.grab_set()

        # Success icon
        ctk.CTkLabel(dialog, text="✅", font=("Arial", 60)).pack(pady=(30, 10))

        ctk.CTkLabel(
            dialog,
            text="Kode Penarikan Berhasil Dibuat!",
            font=("Arial", 16, "bold"),
            text_color="#333333",
        ).pack(pady=(0, 20))

        # Kode frame
        kode_frame = ctk.CTkFrame(dialog, fg_color="#00D26A", corner_radius=12)
        kode_frame.pack(fill="x", padx=30, pady=(0, 20))

        ctk.CTkLabel(
            kode_frame, text="KODE PENARIKAN", font=("Arial", 11), text_color="#FFFFFF"
        ).pack(pady=(15, 5))

        ctk.CTkLabel(
            kode_frame, text=kode, font=("Arial", 28, "bold"), text_color="#FFFFFF"
        ).pack(pady=(0, 15))

        # Detail
        detail_frame = ctk.CTkFrame(dialog, fg_color="#F8F9FA", corner_radius=12)
        detail_frame.pack(fill="x", padx=30, pady=(0, 20))

        details = [
            ("Lokasi", lokasi),
            ("Nominal", f"Rp {nominal:,}".replace(",", ".")),
            ("Biaya Admin", f"Rp {self.biaya_admin:,}".replace(",", ".")),
            ("Total", f"Rp {total:,}".replace(",", ".")),
        ]

        for label, value in details:
            row = ctk.CTkFrame(detail_frame, fg_color="transparent")
            row.pack(fill="x", padx=15, pady=8)

            ctk.CTkLabel(
                row, text=label, font=("Arial", 11), text_color="#666666"
            ).pack(side="left")

            ctk.CTkLabel(
                row, text=value, font=("Arial", 11, "bold"), text_color="#333333"
            ).pack(side="right")

        # Info
        ctk.CTkLabel(
            dialog,
            text="Kode berlaku 15 menit\nGunakan di ATM/Indomaret",
            font=("Arial", 10),
            text_color="#999999",
            justify="center",
        ).pack(pady=(0, 15))

        # Tombol OK
        ctk.CTkButton(
            dialog,
            text="OK, Mengerti",
            font=("Arial", 13, "bold"),
            fg_color="#00D26A",
            hover_color="#00B85C",
            height=45,
            command=dialog.destroy,
        ).pack(fill="x", padx=30, pady=(0, 30))

    def go_back(self):
        messagebox.showinfo("Info", "Kembali ke halaman utama")


if __name__ == "__main__":
    app = WithdrawApp()
    app.mainloop()
