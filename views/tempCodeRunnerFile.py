import customtkinter as ctk
from tkinter import messagebox
import os
import sys


current_dir = os.path.dirname(os.path.abspath(__file__)) 
parent_dir = os.path.dirname(current_dir)                
sys.path.append(parent_dir)                              

try:
    from theme import Theme
except ImportError:

    print("\nCRITICAL ERROR: File theme.py tidak ditemukan di folder root!")
    print(f"Sistem mencari di: {parent_dir}")
    sys.exit(1)


class EditFrame(ctk.CTkFrame):
    def __init__(self, master, field_key, field_title, current_value, save_callback, cancel_callback):
        super().__init__(master, fg_color=Theme.BG)
        self.save_callback = save_callback
        self.cancel_callback = cancel_callback
        self.field_key = field_key
        
        # --- Header Simple ---
        header = ctk.CTkFrame(self, fg_color=Theme.WHITE, height=60, corner_radius=0)
        header.pack(fill="x", pady=(0, 1))

        # Tombol Kembali
        back_btn = ctk.CTkButton(header, text="❮", font=Theme.F_JUMBO, width=50, 
                               fg_color="transparent", text_color=Theme.TEXT, 
                               hover_color=Theme.BTN_GREEN, command=self.cancel_callback)
        back_btn.pack(side="left", pady=10)
        
        title = ctk.CTkLabel(header, text=field_title, font=Theme.F_HEAD, text_color=Theme.TEXT)
        title.pack(side="left", padx=5)

        # Tombol Simpan
        save_header_btn = ctk.CTkButton(header, text="Simpan", font=Theme.F_BTN, width=80,
                                      fg_color="transparent", text_color=Theme.PRIMARY,
                                      hover_color=Theme.BTN_GREEN, command=self.save_action)
        save_header_btn.pack(side="right", padx=10)

        # --- Form Input ---
        form_card = ctk.CTkFrame(self, fg_color=Theme.WHITE, corner_radius=0)
        form_card.pack(fill="x", pady=(20, 0))

        lbl = ctk.CTkLabel(form_card, text=field_title, font=Theme.F_SMALL, text_color=Theme.MUTED)
        lbl.pack(anchor="w", padx=20, pady=(15, 0))

        self.entry = ctk.CTkEntry(form_card, height=45, font=Theme.F_SUB, 
                                fg_color="transparent", border_width=0, text_color=Theme.TEXT)
        self.entry.pack(fill="x", padx=15, pady=(0, 15))
        
        if field_key != "pin":
            self.entry.insert(0, current_value)
        else:
            self.entry.configure(show="•") 

        line = ctk.CTkFrame(form_card, height=2, fg_color=Theme.PRIMARY)
        line.pack(fill="x", side="bottom")

        # --- Hint ---
        hint_text = "Pastikan data yang Anda masukkan benar dan valid."
        if field_key == "pin":
            hint_text = "Jangan berikan PIN Anda kepada siapapun."
            
        hint_lbl = ctk.CTkLabel(self, text=hint_text, font=Theme.F_SMALL, text_color=Theme.MUTED)
        hint_lbl.pack(anchor="w", padx=20, pady=(10, 0))

        self.entry.focus_set()

    def save_action(self):
        new_value = self.entry.get()
        if not new_value:
            messagebox.showwarning("Info", "Data tidak boleh kosong")
            return
        self.save_callback(self.field_key, new_value)


class ProfileFrame(ctk.CTkScrollableFrame):
    def __init__(self, master, user_data, navigate_callback, logout_callback):
        super().__init__(master, fg_color=Theme.BG)
        self.user_data = user_data
        self.navigate = navigate_callback 
        self.logout_callback = logout_callback
        
        self.create_widgets()

    def create_widgets(self):
        # --- Header ---
        header_container = ctk.CTkFrame(self, fg_color=Theme.PRIMARY, corner_radius=0)
        header_container.pack(fill="x", pady=(0, 20))

        profile_circle = ctk.CTkFrame(header_container, width=100, height=100, fg_color=Theme.WHITE, corner_radius=50)
        profile_circle.pack(pady=(30, 10))
        profile_circle.pack_propagate(False)

        initials = "".join([n[0] for n in self.user_data['nama'].split()[:2]]).upper()
        initial_label = ctk.CTkLabel(profile_circle, text=initials, font=Theme.F_HEAD_L, text_color=Theme.PRIMARY)
        initial_label.place(relx=0.5, rely=0.5, anchor="center")

        name_label = ctk.CTkLabel(header_container, text=self.user_data["nama"], font=Theme.F_HEAD, text_color=Theme.WHITE)
        name_label.pack(pady=(5, 5))

        level_label = ctk.CTkLabel(header_container, text=f"⭐ {self.user_data['level']} Member", font=Theme.F_BODY, text_color=Theme.WHITE)
        level_label.pack(pady=(0, 25))

        # --- Menu Items ---
        self.add_section_label("Informasi Akun")
        self.create_menu_item("👤", "Nama Pengguna", "nama", self.user_data["nama"])
        self.create_menu_item("📱", "Nomor Telepon", "no_hp", self.user_data["no_hp"])
        self.create_menu_item("📧", "Email", "email", self.user_data["email"])
        self.create_menu_item("🆔", "E-Saku ID", None, "882910293") 

        self.add_section_label("Keamanan")
        self.create_menu_item("🔒", "Ganti PIN / Password", "pin", "••••••")

        self.add_section_label("Pengaturan")
        self.create_menu_item("🔔", "Notifikasi", None, None, is_setting=True)
        self.create_menu_item("🌐", "Bahasa", None, "Indonesia", is_setting=True)
        self.create_menu_item("❓", "Bantuan", None, None, is_setting=True)

        logout_btn = ctk.CTkButton(self, text="Keluar dari Akun", font=Theme.F_BTN, 
                                   fg_color=Theme.DANGER, hover_color="#FFEBEE", text_color=Theme.DANGER,
                                   height=50, corner_radius=10,
                                   command=self.logout_callback)
        logout_btn.pack(fill="x", padx=20, pady=(40, 50))

    def add_section_label(self, text):
        lbl = ctk.CTkLabel(self, text=text, font=Theme.F_TITLE, text_color=Theme.TEXT)
        lbl.pack(anchor="w", padx=20, pady=(15, 5))

    def create_menu_item(self, icon, title, key_data=None, value_text=None, is_setting=False):
        item_frame = ctk.CTkFrame(self, fg_color=Theme.WHITE, corner_radius=12, border_width=1, border_color="#E0E0E0")
        item_frame.pack(fill="x", padx=20, pady=(0, 10))

        content = ctk.CTkFrame(item_frame, fg_color="transparent")
        content.pack(fill="x", padx=15, pady=15)

        left_box = ctk.CTkFrame(content, fg_color="transparent")
        left_box.pack(side="left", fill="x", expand=True)

        # Ikon
        icon_lbl = ctk.CTkLabel(left_box, text=icon, font=("Segoe UI Emoji", 20), width=35) 
        icon_lbl.pack(side="left", padx=(0, 10))

        text_box = ctk.CTkFrame(left_box, fg_color="transparent")
        text_box.pack(side="left")
        
        title_lbl = ctk.CTkLabel(text_box, text=title, font=Theme.F_BODY, text_color=Theme.TEXT)
        title_lbl.pack(anchor="w")

        if value_text:
            val_lbl = ctk.CTkLabel(text_box, text=value_text, font=Theme.F_SMALL, text_color=Theme.MUTED)
            val_lbl.pack(anchor="w")

        arrow_lbl = ctk.CTkLabel(content, text="›", font=Theme.F_JUMBO, text_color="#CCCCCC")
        
        if key_data or is_setting:
            arrow_lbl.pack(side="right")
            
            def on_tap(event):
                if key_data: self.navigate(key_data, title, value_text)
                elif is_setting: messagebox.showinfo("Info", f"Menu {title}")

            widgets = [item_frame, content, left_box, icon_lbl, text_box, title_lbl, arrow_lbl]
            if value_text: widgets.append(val_lbl if 'val_lbl' in locals() else None)
            
            for w in widgets:
                if w:
                    w.configure(cursor="hand2")
                    w.bind("<Button-1>", on_tap)


class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("DANA Profile")
        self.geometry("520x930") 
        self.resizable(False, False)
        
        try:
            self.configure(fg_color=Theme.BG) 
        except:
            pass

        self.user_data = {
            "nama": "Ahmad Rizki",
            "no_hp": "+62 812-3456-7890",
            "email": "ahmad.rizki@email.com",
            "level": "Gold",
            "pin": "123456" 
        }

        self.current_frame = None
        self.show_profile_page()

    def show_profile_page(self):
        if self.current_frame: self.current_frame.pack_forget()
        self.current_frame = ProfileFrame(self, self.user_data, self.show_edit_page, self.logout)
        self.current_frame.pack(fill="both", expand=True)

    def show_edit_page(self, field_key, field_title, current_value):
        if self.current_frame: self.current_frame.pack_forget()
        val_to_send = current_value if field_key != "pin" else ""
        self.current_frame = EditFrame(self, field_key, field_title, val_to_send, self.save_data, self.show_profile_page)
        self.current_frame.pack(fill="both", expand=True)

    def save_data(self, key, new_value):
        self.user_data[key] = new_value
        messagebox.showinfo("Sukses", "Data berhasil diperbarui!")
        self.show_profile_page()

    def logout(self):
        if messagebox.askyesno("Keluar", "Yakin ingin keluar?"):
            self.quit()

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()