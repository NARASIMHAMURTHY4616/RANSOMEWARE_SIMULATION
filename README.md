# RANSOMEWARE_SIMULATION
its a  ransom ware simulation to discribe how a ransom ware attacks system and to understand how to defend our systems
# 🔐 Ransomware Simulation – AES-256-GCM (Educational Project)

⚠️ **DISCLAIMER – EDUCATIONAL USE ONLY**  
This project simulates ransomware behavior for learning and cybersecurity research.  
Do NOT use this tool on systems, devices, or networks without full permission.
Unauthorized use may result in legal consequences.

---

## 📌 Overview

This project demonstrates how file-encrypting ransomware works in a controlled, harmless environment.  

The project performs the following operations:

- Encrypts files in a target directory using AES-256 GCM
- Deletes the original unencrypted files
- Generates a ransom popup requesting payment
- Reveals the secret key only after correct input
- Includes a second script that decrypts files safely

The purpose of this simulation is to gain practical knowledge of:

- file encryption
- key handling
- ransomware workflow
- authenticated encryption modes
- secure cryptographic programming

---

## 📂 Project Structure
```
ransomware-simulator/
│
├── encryptor.py # encryption + popup ransomware simulation
├── decryptor.py # decrypts locked files
│
└── TESTFILES/ # files targeted for encryption
├── dummy1.txt
├── dummy2.png
└── encryption_key.bin # generated automatically ```

Important:  
- Place only dummy files inside TESTFILES  
- Scripts must stay outside TESTFILES  
```
---

## 🔑 Key Features

✔ AES-256 GCM encryption (strong + authenticated)  
✔ per-file random nonce generation  
✔ file deletion mimics real ransomware  
✔ ransom GUI popup using Tkinter  
✔ copies decryption key to clipboard  
✔ decryptor loads key from:
- encryption_key.bin  
- user input  
- clipboard (tkinter + xclip fallback)  

---

## ⚙️ Requirements

- Python 3.8+
- cryptography package  

Install dependency:

 ` bash` 
 ```pip install cryptography ```
## ▶️ Usage
🔹 Step 1 – Create TESTFILES
```mkdir ~/TESTFILES ```
Add dummy files into it.

🔹 Step 2 – Run Encryption
```python3 encryptor.py```


#### After running:

all files inside TESTFILES become locked `.locked`

original files are removed

`encryption_key.bin` is created

ransom popup appears

correct amount reveals hex key
its default dummy pop up amount  is `10000`
