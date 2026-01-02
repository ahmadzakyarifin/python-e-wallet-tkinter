import customtkinter as ctk
from tkinter import messagebox
from theme import Theme

# Import Views
try:
    from views.home import HomeView
    from views.history import HistoryView
    from views.profile import ProfileFrame 
except ImportError as e:
    print(f"Error Import View: {e}")

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("E-Wallet Pro")
        
        self.W, self.H = 520, 930
        self.center_window()
        self.root.resizable(False, False)
        
        try:
            self.root.configure(fg_color=Theme.BG)
        except:
            pass

        # --- DATA STORE (Backend Simulation) ---
        # Data ini nantinya akan diambil dari database/API
        self.user_data = {
            # 1. Data Profil
            "nama": "Ahmad Rizki",
            "no_hp": "+62 812-3456-7890",
            "email": "ahmad.rizki@email.com",
            "level": "Gold",
            "pin": "123456",
            
            # 2. Data Keuangan (Home)
            "saldo": 2500000,
            "pemasukan": 5000000,
            "pengeluaran": 2500000,
            "limit_trx": 40000000,

            # 3. Data Riwayat (History) - Pindahan dari history.py
            "riwayat_transaksi": [
                {"title": "Gaji Bulanan", "date": "25 Des, 09:00", "amount": 5000000, "type": "in"},
                {"title": "Starbucks Kopi", "date": "24 Des, 14:30", "amount": 55000,   "type": "out"},
                {"title": "Token Listrik", "date": "23 Des, 19:15", "amount": 150000,  "type": "out"},
                {"title": "Beli Pulsa",    "date": "22 Des, 10:00", "amount": 50000,   "type": "out"},
                {"title": "Top Up GoPay",  "date": "20 Des, 08:45", "amount": 100000,  "type": "out"},
                {"title": "Bonus Tahunan", "date": "19 Des, 16:20", "amount": 2000000, "type": "in"},
                {"title": "Bayar Cicilan", "date": "18 Des, 20:00", "amount": 200000,  "type": "out"},
            ]
        }
        # ----------------------------------------

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

    # --- FUNGSI BACKEND ---
    def handle_update_profile(self, key, value):
        print(f"[BACKEND] Mengupdate {key} menjadi {value}")
        self.user_data[key] = value 
        self.show_page("profile")

    def handle_logout(self):
        if messagebox.askyesno("Keluar", "Yakin ingin keluar?"):
            self.root.quit()

    def handle_edit_req(self, field_key, field_title, current_value):
        if isinstance(self.current_active_frame, ProfileFrame):
            self.current_active_frame.show_edit_page(field_key, field_title, current_value, self.handle_update_profile)

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
            
            # PERUBAHAN DI SINI:
            # Ambil list transaksi dari user_data dan kirim ke HistoryView
            data_trx = self.user_data.get("riwayat_transaksi", [])
            view = HistoryView(self.canvas, self.W, self.H, self.show_page, data_trx)
            view.draw()

        elif page_name == "profile":
            self.current_active_frame = ProfileFrame(
                master=self.main_container,
                user_data=self.user_data,
                navigate_callback=self.handle_edit_req,
                logout_callback=self.handle_logout,
                back_to_home_callback=lambda: self.show_page("home")
            )
            self.current_active_frame.pack(fill="both", expand=True)

        elif page_name.startswith("fitur_"):
            messagebox.showinfo("Fitur", f"Buka Halaman {page_name}")
            self.show_page("home")

if __name__ == "__main__":
    ctk.set_appearance_mode("Light")
    root = ctk.CTk()
    app = MainApp(root)
    root.mainloop()