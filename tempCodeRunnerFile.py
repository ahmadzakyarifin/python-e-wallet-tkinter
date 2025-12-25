import tkinter as tk
from tkinter import messagebox
from theme import Theme
from views.home import HomeView
from views.history import HistoryView

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("E-Wallet Pro")
        
        self.W, self.H = 520, 930
        self.center_window()
        self.root.resizable(False, False)
        
        self.canvas = tk.Canvas(self.root, width=self.W, height=self.H, bg=Theme.BG, highlightthickness=0)
        self.canvas.pack()

        self.show_page("home")

    def center_window(self):
        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()
        x = (screen_w - self.W) // 2
        y = (screen_h - self.H) // 2
        self.root.geometry(f"{self.W}x{self.H}+{x}+{y}")

    def show_page(self, page_name):
        print(f"[LOG] Navigasi ke: {page_name}")
        
        if page_name == "home":
            view = HomeView(self.canvas, self.W, self.H, self.show_page)
            view.draw()
            
        elif page_name == "profile":
            messagebox.showinfo("Navigasi", "Halaman PROFIL belum dibuat.")
            
        elif page_name == "history":
            view = HistoryView(self.canvas, self.W, self.H, self.show_page)
            view.draw()

        elif page_name == "fitur_topup":
            messagebox.showinfo("Fitur", "Buka Halaman Top Up")
        elif page_name == "fitur_transfer":
            messagebox.showinfo("Fitur", "Buka Halaman Transfer")
        elif page_name == "fitur_tarik":
            messagebox.showinfo("Fitur", "Buka Halaman Tarik Tunai")
        elif page_name == "fitur_pulsa":
            messagebox.showinfo("Fitur", "Buka Halaman Pulsa")
        elif page_name == "fitur_listrik":
            messagebox.showinfo("Fitur", "Buka Halaman Token Listrik")

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()