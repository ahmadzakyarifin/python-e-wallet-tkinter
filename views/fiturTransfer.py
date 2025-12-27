import customtkinter as ctk
from tkinter import messagebox
import re


class TransferApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Konfigurasi window
        self.title("E-SAKU - Transfer")
        self.geometry("400x700")
        self.resizable(False, False)

        # Set tema
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("green")

        # Data user
        self.saldo = 1250000
        self.transfer_data = {"nomor": "", "nominal": 0, "catatan": ""}

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
            text="Transfer",
            font=("Arial", 24, "bold"),
            text_color="#FFFFFF",
            anchor="w",
        )
        title_label.pack(anchor="w")

        # Saldo
        saldo_label = ctk.CTkLabel(
            title_frame,
            text=f"Saldo: Rp {self.saldo:,.0f}".replace(",", "."),
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

        # Input Nomor HP / ID
        nomor_label = ctk.CTkLabel(
            form_content,
            text="Nomor HP / ID Penerima",
            font=("Arial", 13, "bold"),
            text_color="#333333",
            anchor="w",
        )
        nomor_label.pack(fill="x", pady=(0, 5))

        self.nomor_entry = ctk.CTkEntry(
            form_content,
            placeholder_text="08xx atau ID E-SAKU",
            height=45,
            font=("Arial", 14),
            border_color="#E0E0E0",
            fg_color="#F8F9FA",
        )
        self.nomor_entry.pack(fill="x", pady=(0, 15))

        # Input Nominal
        nominal_label = ctk.CTkLabel(
            form_content,
            text="Nominal Transfer",
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
            btn = ctk.CTkButton(
                quick_frame,
                text=f"{amount//1000}K",
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

        # Catatan (Optional)
        catatan_label = ctk.CTkLabel(
            form_content,
            text="Catatan (Opsional)",
            font=("Arial", 13, "bold"),
            text_color="#333333",
            anchor="w",
        )
        catatan_label.pack(fill="x", pady=(0, 5))

        self.catatan_entry = ctk.CTkEntry(
            form_content,
            placeholder_text="Contoh: Bayar hutang",
            height=45,
            font=("Arial", 14),
            border_color="#E0E0E0",
            fg_color="#F8F9FA",
        )
        self.catatan_entry.pack(fill="x", pady=(0, 10))

        # Riwayat Transfer Terakhir
        history_label = ctk.CTkLabel(
            main_frame,
            text="Transfer Terakhir",
            font=("Arial", 16, "bold"),
            text_color="#333333",
            anchor="w",
        )
        history_label.pack(fill="x", padx=20, pady=(10, 10))

        # Data riwayat dummy
        recent_transfers = [
            {"nama": "Budi Santoso", "nomor": "081234567890", "avatar": "BS"},
            {"nama": "Siti Nurhaliza", "nomor": "082345678901", "avatar": "SN"},
            {"nama": "Ahmad Yani", "nomor": "083456789012", "avatar": "AY"},
        ]

        for transfer in recent_transfers:
            self.create_history_item(main_frame, transfer)

        # Tombol Transfer
        transfer_btn = ctk.CTkButton(
            main_frame,
            text="Transfer Sekarang",
            font=("Arial", 15, "bold"),
            fg_color="#00D26A",
            hover_color="#00B85C",
            height=55,
            corner_radius=12,
            command=self.process_transfer,
        )
        transfer_btn.pack(fill="x", padx=20, pady=(20, 40))

    def create_history_item(self, parent, data):
        item_frame = ctk.CTkFrame(
            parent,
            fg_color="#FFFFFF",
            corner_radius=12,
            border_width=1,
            border_color="#E0E0E0",
            cursor="hand2",
        )
        item_frame.pack(fill="x", padx=20, pady=(0, 8))

        # Bind click
        item_frame.bind("<Button-1>", lambda e: self.select_recipient(data))

        content_frame = ctk.CTkFrame(item_frame, fg_color="transparent")
        content_frame.pack(fill="x", padx=15, pady=12)
        content_frame.bind("<Button-1>", lambda e: self.select_recipient(data))

        # Avatar
        avatar_frame = ctk.CTkFrame(
            content_frame, width=45, height=45, fg_color="#00D26A", corner_radius=25
        )
        avatar_frame.pack(side="left", padx=(0, 12))
        avatar_frame.pack_propagate(False)

        avatar_label = ctk.CTkLabel(
            avatar_frame,
            text=data["avatar"],
            font=("Arial", 16, "bold"),
            text_color="#FFFFFF",
        )
        avatar_label.place(relx=0.5, rely=0.5, anchor="center")
        avatar_label.bind("<Button-1>", lambda e: self.select_recipient(data))

        # Info
        info_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        info_frame.pack(side="left", fill="both", expand=True)
        info_frame.bind("<Button-1>", lambda e: self.select_recipient(data))

        nama_label = ctk.CTkLabel(
            info_frame,
            text=data["nama"],
            font=("Arial", 13, "bold"),
            text_color="#333333",
            anchor="w",
        )
        nama_label.pack(anchor="w", fill="x")
        nama_label.bind("<Button-1>", lambda e: self.select_recipient(data))

        nomor_label = ctk.CTkLabel(
            info_frame,
            text=data["nomor"],
            font=("Arial", 11),
            text_color="#999999",
            anchor="w",
        )
        nomor_label.pack(anchor="w", fill="x")
        nomor_label.bind("<Button-1>", lambda e: self.select_recipient(data))

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

    def select_recipient(self, data):
        self.nomor_entry.delete(0, "end")
        self.nomor_entry.insert(0, data["nomor"])
        messagebox.showinfo("Info", f"Penerima dipilih: {data['nama']}")

    def validate_transfer(self):
        nomor = self.nomor_entry.get().strip()
        nominal_str = self.nominal_entry.get().replace(".", "")

        # Validasi nomor
        if not nomor:
            messagebox.showerror("Error", "Nomor HP/ID penerima harus diisi!")
            return False

        # Validasi nominal
        if not nominal_str or not nominal_str.isdigit():
            messagebox.showerror("Error", "Nominal transfer harus diisi dengan angka!")
            return False

        nominal = int(nominal_str)

        if nominal < 10000:
            messagebox.showerror("Error", "Nominal transfer minimal Rp 10.000!")
            return False

        if nominal > self.saldo:
            messagebox.showerror("Error", "Saldo tidak mencukupi!")
            return False

        self.transfer_data["nomor"] = nomor
        self.transfer_data["nominal"] = nominal
        self.transfer_data["catatan"] = self.catatan_entry.get().strip()

        return True

    def process_transfer(self):
        if not self.validate_transfer():
            return

        # Konfirmasi
        message = f"Transfer ke {self.transfer_data['nomor']}\n"
        message += f"Nominal: Rp {self.transfer_data['nominal']:,}".replace(",", ".")
        if self.transfer_data["catatan"]:
            message += f"\nCatatan: {self.transfer_data['catatan']}"
        message += "\n\nLanjutkan transfer?"

        response = messagebox.askyesno("Konfirmasi Transfer", message)

        if response:
            # Proses transfer
            self.saldo -= self.transfer_data["nominal"]

            messagebox.showinfo(
                "Berhasil",
                f"Transfer berhasil!\n\n"
                f"Nominal: Rp {self.transfer_data['nominal']:,}".replace(",", ".")
                + "\n"
                f"Saldo tersisa: Rp {self.saldo:,}".replace(",", "."),
            )

            # Reset form
            self.nomor_entry.delete(0, "end")
            self.nominal_entry.delete(0, "end")
            self.catatan_entry.delete(0, "end")

            # Update saldo di header
            self.update_saldo_display()

    def update_saldo_display(self):
        # Update tampilan saldo (perlu refresh widget)
        self.destroy()
        new_app = TransferApp()
        new_app.saldo = self.saldo
        new_app.mainloop()

    def go_back(self):
        messagebox.showinfo("Info", "Kembali ke halaman utama")


if __name__ == "__main__":
    app = TransferApp()
    app.mainloop()