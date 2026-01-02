import customtkinter as ctk
from tkinter import messagebox
import random
import string
from theme import Theme

# Import Views
try:
    from views.home import HomeView
    from views.history import HistoryView
    from views.profile import ProfileFrame
    from views.fiturTransfer import TransferView
    from views.tarikTunai import WithdrawView
    from views.topup import TopUpView
    
    from views.fiturPulsa import PulsaView
    from views.fiturTokenListrik import ListrikView
    
except ImportError as e:
    print(f"Error Import View: {e}")

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("E-Wallet Pro")
        
        self.W, self.H = 520, 930
        self.center_window()
        self.root.resizable(False, False)
        
        try: self.root.configure(fg_color=Theme.BG)
        except: pass

        # --- DATA STORE ---
        self.user_data = {
            "nama": "Ahmad Rizki",
            "no_hp": "+62 812-3456-7890",
            "email": "ahmad.rizki@email.com",
            "level": "Gold",
            "pin": "123456",
            "saldo": 2500000,
            "pemasukan": 5000000,
            "pengeluaran": 2500000,
            "limit_trx": 40000000,
            "riwayat_transaksi": [
                {"title": "Gaji Bulanan", "date": "25 Des, 09:00", "amount": 5000000, "type": "in"},
            ]
        }

        self.main_container = ctk.CTkFrame(self.root, fg_color=Theme.BG)
        self.main_container.pack(fill="both", expand=True)

        self.canvas = ctk.CTkCanvas(self.main_container, width=self.W, height=self.H, bg=Theme.BG, highlightthickness=0)
        self.current_active_frame = None

        self.show_page("home")

    def center_window(self):
        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()
        x = (screen_w - self.W) // 2
        y = (screen_h - self.H) // 2
        self.root.geometry(f"{self.W}x{self.H}+{x}+{y}")

    # --- LOGIC BACKEND ---
    def handle_update_profile(self, key, value):
        self.user_data[key] = value 
        self.show_page("profile")

    def handle_logout(self):
        if messagebox.askyesno("Keluar", "Yakin ingin keluar?"):
            self.root.destroy()
            try:
                from login import ESakuApp
                app = ESakuApp()
                app.mainloop()
            except ImportError: pass

    def handle_edit_req(self, field_key, field_title, current_value):
        if isinstance(self.current_active_frame, ProfileFrame):
            self.current_active_frame.show_edit_page(field_key, field_title, current_value, self.handle_update_profile)

    def handle_transfer_process(self, nomor, nominal, catatan):
        if nominal > self.user_data["saldo"]:
            messagebox.showerror("Gagal", "Saldo tidak mencukupi!")
            return
        if messagebox.askyesno("Konfirmasi", f"Transfer Rp {nominal:,} ke {nomor}?"):
            self.user_data["saldo"] -= nominal
            self.user_data["pengeluaran"] += nominal
            self.add_history(f"Trf ke {nomor}", nominal, "out")
            messagebox.showinfo("Sukses", "Transfer Berhasil!")
            self.show_page("home")

    def handle_withdraw_process(self, nominal, biaya_admin, lokasi):
        total = nominal + biaya_admin
        if total > self.user_data["saldo"]:
             messagebox.showerror("Gagal", f"Saldo Kurang!\nTotal: Rp {total:,}")
             return None
        if not messagebox.askyesno("Konfirmasi", f"Tarik Rp {nominal:,} + Admin Rp {biaya_admin:,}?"):
            return None
        self.user_data["saldo"] -= total
        self.user_data["pengeluaran"] += total
        self.add_history(f"Tarik Tunai ({lokasi})", total, "out")
        return "".join(random.choices(string.digits, k=6))

    def handle_ppob_process(self, tipe, data):
        harga = data['harga']
        if harga > self.user_data["saldo"]:
            messagebox.showerror("Gagal", "Saldo tidak mencukupi!")
            return

        judul = "Konfirmasi Beli Pulsa" if tipe == "pulsa" else "Konfirmasi Beli Token"
        detail = f"Nomor: {data.get('nomor', data.get('meter'))}\nHarga: Rp {harga:,}"

        if messagebox.askyesno(judul, f"{detail}\n\nLanjutkan Pembayaran?"):
            self.user_data["saldo"] -= harga
            self.user_data["pengeluaran"] += harga
            hist_title = f"Pulsa {data.get('operator','')} {data.get('nomor','')}" if tipe == "pulsa" else f"Token PLN {data.get('meter')}"
            self.add_history(hist_title, harga, "out")
            
            if tipe == "pulsa":
                messagebox.showinfo("Sukses", "Pulsa sedang diproses!")
            else:
                token = f"{random.randint(1000,9999)}-{random.randint(1000,9999)}-{random.randint(1000,9999)}-{random.randint(1000,9999)}"
                messagebox.showinfo("Sukses", f"Pembelian Berhasil!\n\nKODE TOKEN:\n{token}")
            self.show_page("home")

    def handle_topup_process(self, nominal, metode):
        if messagebox.askyesno("Konfirmasi", f"Top Up Rp {nominal:,}\nMetode: {metode}\n\nLanjutkan?"):
            if metode == "Minimarket":
                kode = f"88{random.randint(10000000, 99999999)}"
                messagebox.showinfo("Kode Bayar", f"Tunjukkan kode ini ke Kasir:\n\n{kode}")
            elif metode == "Virtual Account":
                va = f"1122{random.randint(10000000, 99999999)}"
                messagebox.showinfo("Nomor VA", f"Nomor Virtual Account:\n\n{va}")
            
            self.user_data["saldo"] += nominal
            self.user_data["pemasukan"] += nominal
            self.add_history(f"Top Up ({metode})", nominal, "in")
            messagebox.showinfo("Sukses", "Saldo Berhasil Ditambahkan!")
            self.show_page("home")

    def add_history(self, title, amount, type_trx):
        import datetime
        tgl = datetime.datetime.now().strftime("%d %b, %H:%M")
        self.user_data["riwayat_transaksi"].insert(0, {
            "title": title, "date": tgl, "amount": amount, "type": type_trx
        })

    # --- NAVIGASI ---
    def clear_screen(self):
        self.canvas.pack_forget()
        if self.current_active_frame:
            self.current_active_frame.destroy()
            self.current_active_frame = None

    def show_page(self, page_name):
        print(f"[LOG] Navigasi ke: {page_name}")
        self.clear_screen()

        if page_name == "home":
            self.canvas.pack()
            self.canvas.delete("all")
            view = HomeView(self.canvas, self.W, self.H, self.show_page, self.user_data)
            view.draw()
            
        elif page_name == "history":
            self.canvas.pack()
            self.canvas.delete("all")
            data_trx = self.user_data.get("riwayat_transaksi", [])
            view = HistoryView(self.canvas, self.W, self.H, self.show_page, data_trx)
            view.draw()

        elif page_name == "profile":
            self.current_active_frame = ProfileFrame(
                master=self.main_container, user_data=self.user_data,
                navigate_callback=self.handle_edit_req, logout_callback=self.handle_logout,
                back_to_home_callback=lambda: self.show_page("home")
            )
            self.current_active_frame.pack(fill="both", expand=True)

        elif page_name == "fitur_transfer":
            self.current_active_frame = TransferView(
                master=self.main_container, user_data=self.user_data,
                navigate_callback=self.show_page, transfer_callback=self.handle_transfer_process
            )
            self.current_active_frame.pack(fill="both", expand=True)

        elif page_name == "fitur_tarik":
            self.current_active_frame = WithdrawView(
                master=self.main_container, user_data=self.user_data,
                navigate_callback=self.show_page, withdraw_callback=self.handle_withdraw_process
            )
            self.current_active_frame.pack(fill="both", expand=True)

        elif page_name == "fitur_topup":
            self.current_active_frame = TopUpView(
                master=self.main_container, user_data=self.user_data,
                navigate_callback=self.show_page, topup_callback=self.handle_topup_process
            )
            self.current_active_frame.pack(fill="both", expand=True)

        elif page_name == "fitur_pulsa":
            self.current_active_frame = PulsaView(
                master=self.main_container, user_data=self.user_data,
                navigate_callback=self.show_page, transaction_callback=self.handle_ppob_process
            )
            self.current_active_frame.pack(fill="both", expand=True)

        elif page_name == "fitur_listrik":
            self.current_active_frame = ListrikView(
                master=self.main_container, user_data=self.user_data,
                navigate_callback=self.show_page, transaction_callback=self.handle_ppob_process
            )
            self.current_active_frame.pack(fill="both", expand=True)

        elif page_name.startswith("fitur_"):
            messagebox.showinfo("Fitur", f"Halaman {page_name} belum dibuat")
            self.show_page("home")

if __name__ == "__main__":
    ctk.set_appearance_mode("Light")
    root = ctk.CTk()
    app = MainApp(root)
    root.mainloop()