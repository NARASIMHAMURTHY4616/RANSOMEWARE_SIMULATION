#!/usr/bin/env python3
from pathlib import Path
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import sys
import tkinter as tk
import subprocess

# -------------- CONFIG --------------
TARGET_FOLDER = str(Path.home() / "TESTFILES")   # default: ~/TESTFILES
KEY_FILE = "encryption_key.bin"
# -------------------------------------

target = Path(TARGET_FOLDER)
if not target.is_dir():
    raise SystemExit(f"Target folder not found: {TARGET_FOLDER}")

key_path = target / KEY_FILE
key = None

# If key file exists, ask to use it
if key_path.exists():
    use_file = input(f"Key file found at {key_path}. Use it? (Y/n): ").strip().lower()
    if use_file in ("", "y", "yes"):
        key = key_path.read_bytes()
    else:
        key = None

if key is None:
    raw = input("Enter decryption key (hex) or press Enter to read from clipboard: ").strip()
    if raw == "":
        # try reading clipboard with tkinter
        try:
            r = tk.Tk()
            r.withdraw()
            raw = r.clipboard_get().strip()
            r.destroy()
            print("Read key from clipboard.")
        except Exception:
            # fallback to xclip
            try:
                p = subprocess.run(['xclip','-selection','clipboard','-o'], capture_output=True, text=True)
                raw = p.stdout.strip()
                print("Read key from clipboard via xclip.")
            except Exception as e:
                print("Failed to read clipboard:", e)
                sys.exit(1)

    try:
        key = bytes.fromhex(raw)
    except Exception as e:
        print("Invalid hex key:", e)
        sys.exit(1)

if len(key) != 32:
    print("Key must be 32 bytes (256 bits). Provided key length:", len(key))
    sys.exit(1)

aesgcm = AESGCM(key)

decrypted = 0
failed = 0

for entry in list(target.iterdir()):
    if not entry.is_file():
        continue
    if not entry.name.endswith(".locked"):
        continue
    if entry.name == KEY_FILE + ".locked":
        continue

    data = entry.read_bytes()
    if len(data) < 13:
        print("Skipping (too small):", entry.name)
        failed += 1
        continue

    nonce = data[:12]
    ct = data[12:]
    try:
        pt = aesgcm.decrypt(nonce, ct, associated_data=None)
        out_name = entry.name[:-7]
        (target / out_name).write_bytes(pt)
        entry.unlink()
        print(f"Decrypted: {entry.name} -> {out_name}")
        decrypted += 1
    except Exception as e:
        print(f"Failed to decrypt {entry.name}: {e}")
        failed += 1

print(f"Done. Decrypted: {decrypted}, Failed: {failed}")
