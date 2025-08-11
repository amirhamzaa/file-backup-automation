import os
import shutil
from datetime import datetime
import customtkinter as ctk
from tkinter import filedialog, messagebox

# ===== File Categories =====
categories = {
    "Images": ['.jpg', '.jpeg', '.png', '.gif'],
    "Videos": ['.mp4', '.mkv', '.avi', '.mov'],
    "Music": ['.mp3', '.wav', '.flac'],
    "Documents": ['.pdf', '.docx', '.txt', '.xlsx']
}

# ===== Backup Function =====
def backup_files():
    source_dir = source_entry.get()
    backup_root = backup_entry.get()

    if not source_dir or not backup_root:
        messagebox.showerror("Error", "Please select both Source and Backup folder.")
        return

    # Create timestamp folder
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    backup_dir = os.path.join(backup_root, f"backup_{timestamp}")

    try:
        os.makedirs(backup_dir, exist_ok=True)
    except Exception as e:
        messagebox.showerror("Error", f"Could not create backup directory:\n{e}")
        return

    files_copied = 0
    try:
        for root, dirs, files in os.walk(source_dir):
            for file in files:
                file_ext = os.path.splitext(file)[1].lower()
                category_found = False

                for category, extensions in categories.items():
                    if file_ext in extensions:
                        dest_folder = os.path.join(backup_dir, category)
                        category_found = True
                        break

                if not category_found:
                    dest_folder = os.path.join(backup_dir, "Others")

                os.makedirs(dest_folder, exist_ok=True)
                src_path = os.path.join(root, file)
                shutil.copy2(src_path, os.path.join(dest_folder, file))
                files_copied += 1

        messagebox.showinfo("Success", f"Backup completed!\nTotal files copied: {files_copied}")

    except Exception as e:
        messagebox.showerror("Error", f"Backup failed:\n{e}")

# ===== Folder Select =====
def select_source():
    folder = filedialog.askdirectory()
    if folder:
        source_entry.delete(0, ctk.END)
        source_entry.insert(0, folder)

def select_backup():
    folder = filedialog.askdirectory()
    if folder:
        backup_entry.delete(0, ctk.END)
        backup_entry.insert(0, folder)

# ===== Theme Switch =====
def change_theme():
    theme = theme_switch.get()
    if theme == "Light":
        ctk.set_appearance_mode("light")
    else:
        ctk.set_appearance_mode("dark")

# ===== UI Setup =====
ctk.set_appearance_mode("dark")  # default theme
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("File Backup Automation")
app.geometry("500x400")
app.resizable(False, False)

# Title
title_label = ctk.CTkLabel(app, text="📂 File Backup Automation", font=("Arial", 20, "bold"))
title_label.pack(pady=10)

# Source Folder
source_frame = ctk.CTkFrame(app)
source_frame.pack(pady=10, padx=20, fill="x")
source_label = ctk.CTkLabel(source_frame, text="Source Folder:")
source_label.pack(side="left", padx=5)
source_entry = ctk.CTkEntry(source_frame, width=300)
source_entry.pack(side="left", padx=5)
source_btn = ctk.CTkButton(source_frame, text="Browse", command=select_source)
source_btn.pack(side="left", padx=5)

# Backup Folder
backup_frame = ctk.CTkFrame(app)
backup_frame.pack(pady=10, padx=20, fill="x")
backup_label = ctk.CTkLabel(backup_frame, text="Backup Folder:")
backup_label.pack(side="left", padx=5)
backup_entry = ctk.CTkEntry(backup_frame, width=300)
backup_entry.pack(side="left", padx=5)
backup_btn = ctk.CTkButton(backup_frame, text="Browse", command=select_backup)
backup_btn.pack(side="left", padx=5)

# Theme Switch
theme_switch = ctk.CTkOptionMenu(app, values=["Dark", "Light"], command=lambda _: change_theme())
theme_switch.set("Dark")
theme_switch.pack(pady=10)

# Backup Button
backup_btn_main = ctk.CTkButton(app, text="Start Backup", command=backup_files, fg_color="green", hover_color="darkgreen")
backup_btn_main.pack(pady=20)

# Footer
footer_label = ctk.CTkLabel(app, text="Made by Amir Hamza", font=("Arial", 12))
footer_label.pack(side="bottom", pady=10)

app.mainloop()
