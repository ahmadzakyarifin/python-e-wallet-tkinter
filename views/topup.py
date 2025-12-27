import customtkinter as ctk
from tkinter import messagebox
import random


class TopUpApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Konfigurasi window
        self.title("E-SAKU - Top Up")
        self.geometry("400x700")
        self.resizable(False, False)

        # Set tema
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("green")

        # Data user
        self.saldo = 1250000

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
            text="Top Up Saldo",
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
            text="Nominal Top Up",
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

        quick_amounts = [50000, 100000, 200000, 500000]
        for i, amount in enumerate(quick_amounts):
            label = f"{amount//1000}K"
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

        # Metode Pembayaran
        metode_label = ctk.CTkLabel(
            form_content,
            text="Metode Pembayaran",
            font=("Arial", 13, "bold"),
            text_color="#333333",
            anchor="w",
        )
        metode_label.pack(fill="x", pady=(10, 10))

        # Metode options
        payment_methods = [
            {
                "name": "Transfer Bank",
                "icon": "🏦",
                "desc": "BCA, BNI, BRI, Mandiri",
                "fee": "GRATIS",
            },
            {
                "name": "Virtual Account",
                "icon": "💳",
                "desc": "VA otomatis",
                "fee": "GRATIS",
            },
            {
                "name": "Minimarket",
                "icon": "🏪",
                "desc": "Indomaret, Alfamart",
                "fee": "Rp 2.500",
            },
            {
                "name": "E-Wallet",
                "icon": "📱",
                "desc": "OVO, GoPay, ShopeePay",
                "fee": "GRATIS",
            },
        ]

        self.selected_method = None
        self.method_buttons = []

        for method in payment_methods:
            self.create_payment_method(form_content, method)

        # Info
        info_frame = ctk.CTkFrame(form_content, fg_color="#E3F2FD", corner_radius=8)
        info_frame.pack(fill="x", pady=(15, 10))

        info_content = ctk.CTkFrame(info_frame, fg_color="transparent")
        info_content.pack(fill="x", padx=12, pady=10)

        ctk.CTkLabel(info_content, text="ℹ️", font=("Arial", 16)).pack(
            side="left", padx=(0, 8)
        )

        ctk.CTkLabel(
            info_content,
            text="Saldo akan masuk otomatis setelah\npembayaran dikonfirmasi (1-5 menit)",
            font=("Arial", 10),
            text_color="#1976D2",
            anchor="w",
            justify="left",
        ).pack(side="left", fill="x", expand=True)

        # Riwayat Top Up
        history_label = ctk.CTkLabel(
            main_frame,
            text="Riwayat Top Up",
            font=("Arial", 16, "bold"),
            text_color="#333333",
            anchor="w",
        )
        history_label.pack(fill="x", padx=20, pady=(10, 10))

        # Data riwayat dummy
        recent_topups = [
            {
                "metode": "Transfer BCA",
                "nominal": 500000,
                "tanggal": "25 Des 2024",
                "status": "Berhasil",
            },
            {
                "metode": "Indomaret",
                "nominal": 200000,
                "tanggal": "20 Des 2024",
                "status": "Berhasil",
            },
            {
                "metode": "Virtual Account",
                "nominal": 300000,
                "tanggal": "15 Des 2024",
                "status": "Berhasil",
            },
        ]

        for topup in recent_topups:
            self.create_history_item(main_frame, topup)

        # Tombol Top Up
        topup_btn = ctk.CTkButton(
            main_frame,
            text="Lanjutkan Top Up",
            font=("Arial", 15, "bold"),
            fg_color="#00D26A",
            hover_color="#00B85C",
            height=55,
            corner_radius=12,
            command=self.process_topup,
        )
        topup_btn.pack(fill="x", padx=20, pady=(20, 40))

    def create_payment_method(self, parent, method):
        item_frame = ctk.CTkFrame(
            parent,
            fg_color="#FFFFFF",
            corner_radius=12,
            border_width=2,
            border_color="#E0E0E0",
            cursor="hand2",
        )
        item_frame.pack(fill="x", pady=(0, 8))

        # Bind click
        item_frame.bind(
            "<Button-1>", lambda e: self.select_method(method["name"], item_frame)
        )

        content_frame = ctk.CTkFrame(item_frame, fg_color="transparent")
        content_frame.pack(fill="x", padx=15, pady=12)
        content_frame.bind(
            "<Button-1>", lambda e: self.select_method(method["name"], item_frame)
        )

        # Icon
        icon_label = ctk.CTkLabel(
            content_frame, text=method["icon"], font=("Arial", 24)
        )
        icon_label.pack(side="left", padx=(0, 12))
        icon_label.bind(
            "<Button-1>", lambda e: self.select_method(method["name"], item_frame)
        )

        # Info
        info_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        info_frame.pack(side="left", fill="both", expand=True)
        info_frame.bind(
            "<Button-1>", lambda e: self.select_method(method["name"], item_frame)
        )

        name_label = ctk.CTkLabel(
            info_frame,
            text=method["name"],
            font=("Arial", 13, "bold"),
            text_color="#333333",
            anchor="w",
        )
        name_label.pack(anchor="w", fill="x")
        name_label.bind(
            "<Button-1>", lambda e: self.select_method(method["name"], item_frame)
        )

        desc_label = ctk.CTkLabel(
            info_frame,
            text=method["desc"],
            font=("Arial", 10),
            text_color="#999999",
            anchor="w",
        )
        desc_label.pack(anchor="w", fill="x")
        desc_label.bind(
            "<Button-1>", lambda e: self.select_method(method["name"], item_frame)
        )

        # Fee
        fee_color = "#00D26A" if method["fee"] == "GRATIS" else "#F57C00"
        fee_label = ctk.CTkLabel(
            content_frame,
            text=method["fee"],
            font=("Arial", 11, "bold"),
            text_color=fee_color,
        )
        fee_label.pack(side="right")
        fee_label.bind(
            "<Button-1>", lambda e: self.select_method(method["name"], item_frame)
        )

        # Simpan referensi
        self.method_buttons.append({"name": method["name"], "frame": item_frame})

    def select_method(self, method_name, frame):
        # Reset semua border
        for btn in self.method_buttons:
            btn["frame"].configure(border_color="#E0E0E0")

        # Highlight yang dipilih
        frame.configure(border_color="#00D26A")
        self.selected_method = method_name

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

        icon_label = ctk.CTkLabel(icon_frame, text="💰", font=("Arial", 20))
        icon_label.place(relx=0.5, rely=0.5, anchor="center")

        # Info
        info_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        info_frame.pack(side="left", fill="both", expand=True)

        metode_label = ctk.CTkLabel(
            info_frame,
            text=data["metode"],
            font=("Arial", 13, "bold"),
            text_color="#333333",
            anchor="w",
        )
        metode_label.pack(anchor="w", fill="x")

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
            text=f"+Rp {data['nominal']:,}".replace(",", "."),
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

    def validate_topup(self):
        nominal_str = self.nominal_entry.get().replace(".", "")

        # Validasi nominal
        if not nominal_str or not nominal_str.isdigit():
            messagebox.showerror("Error", "Nominal top up harus diisi dengan angka!")
            return False

        nominal = int(nominal_str)

        if nominal < 10000:
            messagebox.showerror("Error", "Nominal top up minimal Rp 10.000!")
            return False

        if nominal > 10000000:
            messagebox.showerror("Error", "Nominal top up maksimal Rp 10.000.000!")
            return False

        # Validasi metode
        if not self.selected_method:
            messagebox.showerror("Error", "Pilih metode pembayaran terlebih dahulu!")
            return False

        return nominal

    def process_topup(self):
        nominal = self.validate_topup()
        if not nominal:
            return

        # Konfirmasi
        message = f"Top Up Saldo\n\n"
        message += f"Nominal: Rp {nominal:,}".replace(",", ".") + "\n"
        message += f"Metode: {self.selected_method}\n\n"
        message += "Lanjutkan ke pembayaran?"

        response = messagebox.askyesno("Konfirmasi Top Up", message)

        if response:
            # Generate nomor VA atau kode pembayaran
            if "Virtual Account" in self.selected_method:
                self.show_va_payment(nominal)
            elif "Transfer Bank" in self.selected_method:
                self.show_bank_transfer(nominal)
            elif "Minimarket" in self.selected_method:
                self.show_minimarket_code(nominal)
            else:
                self.show_ewallet_payment(nominal)

    def show_va_payment(self, nominal):
        """Dialog Virtual Account"""
        dialog = ctk.CTkToplevel(self)
        dialog.title("Virtual Account")
        dialog.geometry("350x400")
        dialog.resizable(False, False)
        dialog.grab_set()

        # Icon
        ctk.CTkLabel(dialog, text="💳", font=("Arial", 60)).pack(pady=(30, 10))

        ctk.CTkLabel(
            dialog,
            text="Nomor Virtual Account",
            font=("Arial", 16, "bold"),
            text_color="#333333",
        ).pack(pady=(0, 20))

        # VA Number
        va_number = f"8808{random.randint(100000000, 999999999)}"
        va_frame = ctk.CTkFrame(dialog, fg_color="#00D26A", corner_radius=12)
        va_frame.pack(fill="x", padx=30, pady=(0, 20))

        ctk.CTkLabel(
            va_frame, text=va_number, font=("Arial", 24, "bold"), text_color="#FFFFFF"
        ).pack(pady=20)

        # Detail
        detail_frame = ctk.CTkFrame(dialog, fg_color="#F8F9FA", corner_radius=12)
        detail_frame.pack(fill="x", padx=30, pady=(0, 20))

        ctk.CTkLabel(
            detail_frame, text="Nominal", font=("Arial", 11), text_color="#666666"
        ).pack(pady=(15, 5))

        ctk.CTkLabel(
            detail_frame,
            text=f"Rp {nominal:,}".replace(",", "."),
            font=("Arial", 18, "bold"),
            text_color="#00D26A",
        ).pack(pady=(0, 15))

        # Info
        ctk.CTkLabel(
            dialog,
            text="Transfer ke nomor VA di atas\nmelalui m-banking atau ATM",
            font=("Arial", 10),
            text_color="#999999",
            justify="center",
        ).pack(pady=(0, 15))

        # Tombol
        ctk.CTkButton(
            dialog,
            text="OK",
            font=("Arial", 13, "bold"),
            fg_color="#00D26A",
            hover_color="#00B85C",
            height=45,
            command=dialog.destroy,
        ).pack(fill="x", padx=30, pady=(0, 30))

    def show_bank_transfer(self, nominal):
        """Dialog Transfer Bank"""
        messagebox.showinfo(
            "Transfer Bank",
            f"Silakan transfer ke:\n\n"
            f"Bank BCA\n"
            f"No. Rek: 1234567890\n"
            f"A.n: E-SAKU Indonesia\n\n"
            f"Nominal: Rp {nominal:,}".replace(",", ".") + "\n\n"
            f"Upload bukti transfer di menu Riwayat",
        )

    def show_minimarket_code(self, nominal):
        """Dialog Kode Minimarket"""
        dialog = ctk.CTkToplevel(self)
        dialog.title("Kode Pembayaran")
        dialog.geometry("350x400")
        dialog.resizable(False, False)
        dialog.grab_set()

        # Icon
        ctk.CTkLabel(dialog, text="🏪", font=("Arial", 60)).pack(pady=(30, 10))

        ctk.CTkLabel(
            dialog,
            text="Kode Pembayaran Minimarket",
            font=("Arial", 16, "bold"),
            text_color="#333333",
        ).pack(pady=(0, 20))

        # Code
        payment_code = f"{random.randint(100000000000, 999999999999)}"
        code_frame = ctk.CTkFrame(dialog, fg_color="#00D26A", corner_radius=12)
        code_frame.pack(fill="x", padx=30, pady=(0, 20))

        ctk.CTkLabel(
            code_frame,
            text=payment_code,
            font=("Arial", 24, "bold"),
            text_color="#FFFFFF",
        ).pack(pady=20)

        # Detail
        detail_frame = ctk.CTkFrame(dialog, fg_color="#F8F9FA", corner_radius=12)
        detail_frame.pack(fill="x", padx=30, pady=(0, 20))

        items = [
            ("Nominal", f"Rp {nominal:,}".replace(",", ".")),
            ("Biaya Admin", "Rp 2.500"),
            ("Total", f"Rp {nominal + 2500:,}".replace(",", ".")),
        ]

        for label, value in items:
            row = ctk.CTkFrame(detail_frame, fg_color="transparent")
            row.pack(fill="x", padx=15, pady=5)

            ctk.CTkLabel(
                row, text=label, font=("Arial", 11), text_color="#666666"
            ).pack(side="left")

            ctk.CTkLabel(
                row, text=value, font=("Arial", 11, "bold"), text_color="#333333"
            ).pack(side="right")

        # Info
        ctk.CTkLabel(
            dialog,
            text="Tunjukkan kode ini ke kasir\nIndomaret atau Alfamart",
            font=("Arial", 10),
            text_color="#999999",
            justify="center",
        ).pack(pady=(10, 15))

        # Tombol
        ctk.CTkButton(
            dialog,
            text="OK",
            font=("Arial", 13, "bold"),
            fg_color="#00D26A",
            hover_color="#00B85C",
            height=45,
            command=dialog.destroy,
        ).pack(fill="x", padx=30, pady=(0, 30))

    def show_ewallet_payment(self, nominal):
        """Dialog E-Wallet"""
        messagebox.showinfo(
            "E-Wallet",
            f"Anda akan diarahkan ke aplikasi {self.selected_method}\n\n"
            f"Nominal: Rp {nominal:,}".replace(",", ".") + "\n\n"
            f"Klik OK untuk melanjutkan",
        )

    def go_back(self):
        messagebox.showinfo("Info", "Kembali ke halaman utama")


if __name__ == "__main__":
    app = TopUpApp()
    app.mainloop()
