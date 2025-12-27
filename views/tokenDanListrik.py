import customtkinter as ctk
from tkinter import messagebox


class PulsaListrikApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Konfigurasi window
        self.title("E-SAKU - Pulsa & Listrik")
        self.geometry("400x700")
        self.resizable(False, False)

        # Set tema
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("green")

        # Data user
        self.saldo = 1250000
        self.current_tab = "pulsa"  # pulsa atau listrik

        self.create_widgets()

    def create_widgets(self):
        # Main container
        main_frame = ctk.CTkFrame(self, fg_color="#F8F9FA")
        main_frame.pack(fill="both", expand=True)

        # Header
        header_frame = ctk.CTkFrame(
            main_frame, fg_color="#00D26A", corner_radius=0, height=120
        )
        header_frame.pack(fill="x")
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
            text="Pulsa & Listrik",
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

        # Tab Switcher
        tab_frame = ctk.CTkFrame(main_frame, fg_color="#FFFFFF", height=60)
        tab_frame.pack(fill="x", padx=20, pady=(20, 20))
        tab_frame.pack_propagate(False)

        tab_container = ctk.CTkFrame(tab_frame, fg_color="transparent")
        tab_container.pack(expand=True)

        self.pulsa_btn = ctk.CTkButton(
            tab_container,
            text="📱 Pulsa",
            width=150,
            height=45,
            font=("Arial", 14, "bold"),
            fg_color="#00D26A",
            hover_color="#00B85C",
            command=lambda: self.switch_tab("pulsa"),
        )
        self.pulsa_btn.pack(side="left", padx=(0, 5))

        self.listrik_btn = ctk.CTkButton(
            tab_container,
            text="⚡ Listrik",
            width=150,
            height=45,
            font=("Arial", 14, "bold"),
            fg_color="#E0E0E0",
            text_color="#666666",
            hover_color="#D0D0D0",
            command=lambda: self.switch_tab("listrik"),
        )
        self.listrik_btn.pack(side="left")

        # Content Frame (scrollable)
        self.content_frame = ctk.CTkScrollableFrame(main_frame, fg_color="#F8F9FA")
        self.content_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        # Load konten awal
        self.load_pulsa_content()

    def switch_tab(self, tab):
        self.current_tab = tab

        # Update button styles
        if tab == "pulsa":
            self.pulsa_btn.configure(fg_color="#00D26A", text_color="#FFFFFF")
            self.listrik_btn.configure(fg_color="#E0E0E0", text_color="#666666")
            self.load_pulsa_content()
        else:
            self.pulsa_btn.configure(fg_color="#E0E0E0", text_color="#666666")
            self.listrik_btn.configure(fg_color="#00D26A", text_color="#FFFFFF")
            self.load_listrik_content()

    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def load_pulsa_content(self):
        self.clear_content()

        # Form Container
        form_frame = ctk.CTkFrame(
            self.content_frame,
            fg_color="#FFFFFF",
            corner_radius=15,
            border_width=1,
            border_color="#E0E0E0",
        )
        form_frame.pack(fill="x", pady=(0, 20))

        form_content = ctk.CTkFrame(form_frame, fg_color="transparent")
        form_content.pack(fill="x", padx=20, pady=20)

        # Input Nomor HP
        nomor_label = ctk.CTkLabel(
            form_content,
            text="Nomor HP",
            font=("Arial", 13, "bold"),
            text_color="#333333",
            anchor="w",
        )
        nomor_label.pack(fill="x", pady=(0, 5))

        self.nomor_entry = ctk.CTkEntry(
            form_content,
            placeholder_text="08xx xxxx xxxx",
            height=45,
            font=("Arial", 14),
            border_color="#E0E0E0",
            fg_color="#F8F9FA",
        )
        self.nomor_entry.pack(fill="x", pady=(0, 15))

        # Operator
        operator_label = ctk.CTkLabel(
            form_content,
            text="Pilih Operator",
            font=("Arial", 13, "bold"),
            text_color="#333333",
            anchor="w",
        )
        operator_label.pack(fill="x", pady=(0, 10))

        operators = [
            {"name": "Telkomsel", "color": "#E60012"},
            {"name": "Indosat", "color": "#FFD100"},
            {"name": "XL Axiata", "color": "#0095DA"},
            {"name": "Tri", "color": "#FF6B00"},
        ]

        operator_container = ctk.CTkFrame(form_content, fg_color="transparent")
        operator_container.pack(fill="x", pady=(0, 15))

        self.selected_operator = None
        self.operator_buttons = []

        for i, op in enumerate(operators):
            btn = ctk.CTkButton(
                operator_container,
                text=op["name"],
                width=80,
                height=40,
                font=("Arial", 11, "bold"),
                fg_color="#F0F0F0",
                text_color="#666666",
                hover_color="#E0E0E0",
                border_width=2,
                border_color="#E0E0E0",
                command=lambda o=op["name"], b=None: self.select_operator(o),
            )
            btn.pack(side="left", padx=(0, 8) if i < 3 else 0, expand=True, fill="x")
            self.operator_buttons.append(btn)

        # Nominal Pulsa
        nominal_label = ctk.CTkLabel(
            form_content,
            text="Pilih Nominal",
            font=("Arial", 13, "bold"),
            text_color="#333333",
            anchor="w",
        )
        nominal_label.pack(fill="x", pady=(10, 10))

        # Paket pulsa
        pulsa_packages = [
            {"nominal": 5000, "harga": 6500},
            {"nominal": 10000, "harga": 11500},
            {"nominal": 15000, "harga": 16500},
            {"nominal": 20000, "harga": 21500},
            {"nominal": 25000, "harga": 26500},
            {"nominal": 50000, "harga": 51500},
            {"nominal": 100000, "harga": 101500},
            {"nominal": 150000, "harga": 151500},
        ]

        self.selected_pulsa = None
        self.pulsa_buttons = []

        for package in pulsa_packages:
            self.create_pulsa_package(form_content, package)

        # Tombol Beli
        self.buy_btn = ctk.CTkButton(
            self.content_frame,
            text="Beli Pulsa",
            font=("Arial", 15, "bold"),
            fg_color="#00D26A",
            hover_color="#00B85C",
            height=55,
            corner_radius=12,
            command=self.buy_pulsa,
        )
        self.buy_btn.pack(fill="x", pady=(10, 20))

    def load_listrik_content(self):
        self.clear_content()

        # Form Container
        form_frame = ctk.CTkFrame(
            self.content_frame,
            fg_color="#FFFFFF",
            corner_radius=15,
            border_width=1,
            border_color="#E0E0E0",
        )
        form_frame.pack(fill="x", pady=(0, 20))

        form_content = ctk.CTkFrame(form_frame, fg_color="transparent")
        form_content.pack(fill="x", padx=20, pady=20)

        # Input Nomor Meter
        meter_label = ctk.CTkLabel(
            form_content,
            text="Nomor Meter / ID Pelanggan",
            font=("Arial", 13, "bold"),
            text_color="#333333",
            anchor="w",
        )
        meter_label.pack(fill="x", pady=(0, 5))

        self.meter_entry = ctk.CTkEntry(
            form_content,
            placeholder_text="Masukkan nomor meter",
            height=45,
            font=("Arial", 14),
            border_color="#E0E0E0",
            fg_color="#F8F9FA",
        )
        self.meter_entry.pack(fill="x", pady=(0, 15))

        # Info pelanggan (dummy)
        info_frame = ctk.CTkFrame(form_content, fg_color="#E3F2FD", corner_radius=8)
        info_frame.pack(fill="x", pady=(0, 15))

        info_content = ctk.CTkFrame(info_frame, fg_color="transparent")
        info_content.pack(fill="x", padx=12, pady=10)

        ctk.CTkLabel(info_content, text="ℹ️", font=("Arial", 16)).pack(
            side="left", padx=(0, 8)
        )

        ctk.CTkLabel(
            info_content,
            text="Masukkan nomor meter untuk cek info pelanggan",
            font=("Arial", 10),
            text_color="#1976D2",
            anchor="w",
        ).pack(side="left", fill="x", expand=True)

        # Nominal Token
        nominal_label = ctk.CTkLabel(
            form_content,
            text="Pilih Nominal Token",
            font=("Arial", 13, "bold"),
            text_color="#333333",
            anchor="w",
        )
        nominal_label.pack(fill="x", pady=(10, 10))

        # Paket token
        token_packages = [
            {"nominal": 20000, "admin": 2500},
            {"nominal": 50000, "admin": 2500},
            {"nominal": 100000, "admin": 2500},
            {"nominal": 200000, "admin": 2500},
            {"nominal": 500000, "admin": 2500},
            {"nominal": 1000000, "admin": 2500},
        ]

        self.selected_token = None
        self.token_buttons = []

        for package in token_packages:
            self.create_token_package(form_content, package)

        # Tombol Beli
        self.buy_token_btn = ctk.CTkButton(
            self.content_frame,
            text="Beli Token Listrik",
            font=("Arial", 15, "bold"),
            fg_color="#00D26A",
            hover_color="#00B85C",
            height=55,
            corner_radius=12,
            command=self.buy_token,
        )
        self.buy_token_btn.pack(fill="x", pady=(10, 20))

    def create_pulsa_package(self, parent, package):
        item_frame = ctk.CTkFrame(
            parent,
            fg_color="#FFFFFF",
            corner_radius=10,
            border_width=2,
            border_color="#E0E0E0",
            cursor="hand2",
        )
        item_frame.pack(fill="x", pady=(0, 8))

        # Bind click
        item_frame.bind(
            "<Button-1>", lambda e: self.select_pulsa_package(package, item_frame)
        )

        content_frame = ctk.CTkFrame(item_frame, fg_color="transparent")
        content_frame.pack(fill="x", padx=15, pady=12)
        content_frame.bind(
            "<Button-1>", lambda e: self.select_pulsa_package(package, item_frame)
        )

        # Left - Nominal
        left_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        left_frame.pack(side="left", fill="both", expand=True)
        left_frame.bind(
            "<Button-1>", lambda e: self.select_pulsa_package(package, item_frame)
        )

        nominal_label = ctk.CTkLabel(
            left_frame,
            text=f"Rp {package['nominal']:,}".replace(",", "."),
            font=("Arial", 14, "bold"),
            text_color="#333333",
            anchor="w",
        )
        nominal_label.pack(anchor="w", fill="x")
        nominal_label.bind(
            "<Button-1>", lambda e: self.select_pulsa_package(package, item_frame)
        )

        # Harga
        harga_label = ctk.CTkLabel(
            content_frame,
            text=f"Rp {package['harga']:,}".replace(",", "."),
            font=("Arial", 13, "bold"),
            text_color="#00D26A",
        )
        harga_label.pack(side="right")
        harga_label.bind(
            "<Button-1>", lambda e: self.select_pulsa_package(package, item_frame)
        )

        self.pulsa_buttons.append({"package": package, "frame": item_frame})

    def create_token_package(self, parent, package):
        item_frame = ctk.CTkFrame(
            parent,
            fg_color="#FFFFFF",
            corner_radius=10,
            border_width=2,
            border_color="#E0E0E0",
            cursor="hand2",
        )
        item_frame.pack(fill="x", pady=(0, 8))

        # Bind click
        item_frame.bind(
            "<Button-1>", lambda e: self.select_token_package(package, item_frame)
        )

        content_frame = ctk.CTkFrame(item_frame, fg_color="transparent")
        content_frame.pack(fill="x", padx=15, pady=12)
        content_frame.bind(
            "<Button-1>", lambda e: self.select_token_package(package, item_frame)
        )

        # Left - Nominal
        left_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        left_frame.pack(side="left", fill="both", expand=True)
        left_frame.bind(
            "<Button-1>", lambda e: self.select_token_package(package, item_frame)
        )

        nominal_label = ctk.CTkLabel(
            left_frame,
            text=f"Token Rp {package['nominal']:,}".replace(",", "."),
            font=("Arial", 14, "bold"),
            text_color="#333333",
            anchor="w",
        )
        nominal_label.pack(anchor="w", fill="x")
        nominal_label.bind(
            "<Button-1>", lambda e: self.select_token_package(package, item_frame)
        )

        admin_label = ctk.CTkLabel(
            left_frame,
            text=f"Admin: Rp {package['admin']:,}".replace(",", "."),
            font=("Arial", 10),
            text_color="#999999",
            anchor="w",
        )
        admin_label.pack(anchor="w", fill="x")
        admin_label.bind(
            "<Button-1>", lambda e: self.select_token_package(package, item_frame)
        )

        # Harga total
        total = package["nominal"] + package["admin"]
        harga_label = ctk.CTkLabel(
            content_frame,
            text=f"Rp {total:,}".replace(",", "."),
            font=("Arial", 13, "bold"),
            text_color="#00D26A",
        )
        harga_label.pack(side="right")
        harga_label.bind(
            "<Button-1>", lambda e: self.select_token_package(package, item_frame)
        )

        self.token_buttons.append({"package": package, "frame": item_frame})

    def select_operator(self, operator):
        # Reset semua
        for btn in self.operator_buttons:
            btn.configure(
                fg_color="#F0F0F0", text_color="#666666", border_color="#E0E0E0"
            )

        # Highlight yang dipilih
        for i, btn in enumerate(self.operator_buttons):
            if btn.cget("text") == operator:
                btn.configure(
                    fg_color="#00D26A", text_color="#FFFFFF", border_color="#00D26A"
                )

        self.selected_operator = operator

    def select_pulsa_package(self, package, frame):
        # Reset semua
        for btn in self.pulsa_buttons:
            btn["frame"].configure(border_color="#E0E0E0")

        # Highlight yang dipilih
        frame.configure(border_color="#00D26A")
        self.selected_pulsa = package

    def select_token_package(self, package, frame):
        # Reset semua
        for btn in self.token_buttons:
            btn["frame"].configure(border_color="#E0E0E0")

        # Highlight yang dipilih
        frame.configure(border_color="#00D26A")
        self.selected_token = package

    def buy_pulsa(self):
        nomor = self.nomor_entry.get().strip()

        # Validasi
        if not nomor:
            messagebox.showerror("Error", "Nomor HP harus diisi!")
            return

        if not self.selected_operator:
            messagebox.showerror("Error", "Pilih operator terlebih dahulu!")
            return

        if not self.selected_pulsa:
            messagebox.showerror("Error", "Pilih nominal pulsa terlebih dahulu!")
            return

        if self.selected_pulsa["harga"] > self.saldo:
            messagebox.showerror("Error", "Saldo tidak mencukupi!")
            return

        # Konfirmasi
        message = f"Beli Pulsa\n\n"
        message += f"Nomor: {nomor}\n"
        message += f"Operator: {self.selected_operator}\n"
        message += (
            f"Nominal: Rp {self.selected_pulsa['nominal']:,}".replace(",", ".") + "\n"
        )
        message += (
            f"Harga: Rp {self.selected_pulsa['harga']:,}".replace(",", ".") + "\n\n"
        )
        message += "Lanjutkan pembelian?"

        response = messagebox.askyesno("Konfirmasi Pembelian", message)

        if response:
            self.saldo -= self.selected_pulsa["harga"]
            messagebox.showinfo(
                "Berhasil",
                f"Pulsa berhasil terisi!\n\n"
                f"Nomor: {nomor}\n"
                f"Nominal: Rp {self.selected_pulsa['nominal']:,}".replace(",", ".")
                + "\n\n"
                f"Saldo tersisa: Rp {self.saldo:,}".replace(",", "."),
            )

            # Reset form
            self.nomor_entry.delete(0, "end")
            self.selected_operator = None
            self.selected_pulsa = None

    def buy_token(self):
        meter = self.meter_entry.get().strip()

        # Validasi
        if not meter:
            messagebox.showerror("Error", "Nomor meter harus diisi!")
            return

        if not self.selected_token:
            messagebox.showerror("Error", "Pilih nominal token terlebih dahulu!")
            return

        total = self.selected_token["nominal"] + self.selected_token["admin"]

        if total > self.saldo:
            messagebox.showerror("Error", "Saldo tidak mencukupi!")
            return

        # Konfirmasi
        message = f"Beli Token Listrik\n\n"
        message += f"Nomor Meter: {meter}\n"
        message += (
            f"Nominal: Rp {self.selected_token['nominal']:,}".replace(",", ".") + "\n"
        )
        message += (
            f"Admin: Rp {self.selected_token['admin']:,}".replace(",", ".") + "\n"
        )
        message += f"Total: Rp {total:,}".replace(",", ".") + "\n\n"
        message += "Lanjutkan pembelian?"

        response = messagebox.askyesno("Konfirmasi Pembelian", message)

        if response:
            # Generate token dummy
            import random

            token_code = f"{random.randint(1000, 9999)}-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}"

            self.saldo -= total

            messagebox.showinfo(
                "Berhasil",
                f"Token listrik berhasil dibeli!\n\n"
                f"Nomor Meter: {meter}\n"
                f"Kode Token:\n{token_code}\n\n"
                f"Saldo tersisa: Rp {self.saldo:,}".replace(",", "."),
            )

            # Reset form
            self.meter_entry.delete(0, "end")
            self.selected_token = None

    def go_back(self):
        messagebox.showinfo("Info", "Kembali ke halaman utama")


if __name__ == "__main__":
    app = PulsaListrikApp()
    app.mainloop()
