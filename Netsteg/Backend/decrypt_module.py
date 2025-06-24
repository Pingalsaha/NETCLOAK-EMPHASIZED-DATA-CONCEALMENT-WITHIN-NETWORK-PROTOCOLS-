# decrypt_module.py

import json
from cryptography.fernet import Fernet
import scapy.all as scapy
import os
from datetime import datetime

# Load encryption key
def load_key():
    key_path = "secret.key"
    if os.path.exists(key_path):
        with open(key_path, "rb") as f:
            return f.read()
    raise Exception("Encryption key not found.")

# Decrypt
def decrypt_data(encrypted_data, key):
    cipher = Fernet(key)
    try:
        return cipher.decrypt(encrypted_data).decode()
    except:
        return None

# Match and update decrypted value in history
def update_history_with_decrypted(original_encrypted, decrypted_text):
    file_path = "savedData.json"
    try:
        with open(file_path, "r") as f:
            data = json.load(f)

        updated = False
        for entry in data.get("history", []):
            if entry["encrypted"] == original_encrypted and not entry["decrypted"]:
                entry["decrypted"] = decrypted_text
                updated = True

        if updated:
            with open(file_path, "w") as f:
                json.dump(data, f, indent=2)
            print("🔓 Decrypted data added to history.")
    except Exception as e:
        print(f"Error updating decrypted data: {e}")

# Save raw encrypted content for reference
def log_raw(raw_data):
    file_path = "savedData.json"
    try:
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                data = json.load(f)
        else:
            data = {}

        if "rawData" not in data:
            data["rawData"] = []

        data["rawData"].append(raw_data)

        with open(file_path, "w") as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        print(f"Error logging raw data: {e}")

# Simulated TCP capture and decrypt
def capture_tcp_packets():
    key = load_key()
    print("Sniffing TCP packets for decryption...")

    packets = scapy.sniff(filter="tcp", timeout=15)

    for pkt in packets:
        if pkt.haslayer(scapy.Raw):
            try:
                raw_payload = pkt[scapy.Raw].load.decode(errors="ignore")
                print(f"Captured TCP data: {raw_payload}")
                log_raw(raw_payload)
                decrypted = decrypt_data(raw_payload.encode(), key)
                if decrypted:
                    print("✅ Decrypted:", decrypted)
                    update_history_with_decrypted(raw_payload, decrypted)
            except Exception as e:
                print("⚠️ Decryption failed:", e)

def start_decryption():
    capture_tcp_packets()
    print("🔓 Decryption process completed.")

if __name__ == "__main__":
    start_decryption()
