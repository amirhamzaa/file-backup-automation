import os
import shutil
from datetime import datetime

source_dir = r"C:\Users\AMIR HAMZA\Downloads\Cambridge IELTS 1\Cambridge IELTS 1" 
backup_root = r"C:\Users\AMIR HAMZA\Downloads\Cambridge IELTS 1\backup\backup_2025-08-11_22-03-48\Cambridge IELTS 1" 

categories = {
    "Images": ['.jpg', '.jpeg', '.png', '.gif'],
    "Videos": ['.mp4', '.mkv', '.avi', '.mov'],
    "Music": ['.mp3', '.wav', '.flac'],
    "Documents": ['.pdf', '.docx', '.txt', '.xlsx']
}


timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
backup_dir = os.path.join(backup_root, f"backup_{timestamp}")

try:
    os.makedirs(backup_dir, exist_ok=True)
    print(f"[+] Backup directory created: {backup_dir}")
except Exception as e:
    print(f"[ERROR] Could not create backup directory: {e}")
    exit()


try:
    files_copied = 0
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
            print(f"Copied: {file} → {dest_folder}")

    print(f"\n[✓] Backup completed! Total files copied: {files_copied}")

except Exception as e:
    print(f"[ERROR] Backup process failed: {e}")
