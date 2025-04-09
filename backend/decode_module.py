# decode_module.py

import base64
import json
from cryptography.fernet import Fernet
import scapy.all as scapy
import requests
import dns.resolver
import os

# Log messages to JSON file
def log_message(message):
    file_path = 'savedData.json'
    try:
        # Read existing logs if file exists
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                data = json.load(f)
        else:
            data = {}

        # Initialize logs list if it doesn't exist
        if 'logs' not in data:
            data['logs'] = []

        # Append new message to logs
        data['logs'].append(message)

        # Write updated data back to file
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        print(f"Error logging message: {e}")
        
# Function to load the Fernet key from the file
def load_key():
    key_path = "secret.key"
    if os.path.exists(key_path):
        with open(key_path, "rb") as key_file:
            key = key_file.read()
        return key
    else:
        raise Exception("Encryption key not found. Please run embed_module.py to generate the key.")

# Decrypt data with the Fernet key
def decrypt_data(encrypted_data, key):
    cipher = Fernet(key)
    try:
        decrypted_data = cipher.decrypt(encrypted_data)
        return decrypted_data.decode()
    except Exception:
        return None  # Return None if decryption fails

# Function to retrieve decoded data
decoded_data_list = []

# Decode the data from different protocols (TCP, HTTP, DNS)
def decode_tcp_packet():
    key = load_key()
    print("Decoding TCP packet...")
    # Simulate the process of capturing TCP packets (or use scapy to sniff actual data)
    packet_data = b"gAAAAABnM5E-I_8ZihO1azvMLDcSL8RCyWYAS0tqjrvfAeOf0JrhoAPgEbDNJ-M8kFUv9mhwwljjCHqXRaiFLWQOzkS-_EgN2A=="  # Example encrypted data
    print(f"Captured TCP Packet with data: {packet_data}")
    decrypted_data = decrypt_data(packet_data, key)
    if decrypted_data:
        print("Decoded Data from TCP packet:", decrypted_data)
        decoded_data_list.append(decrypted_data)
    else:
        print("No valid encrypted data found in this TCP packet.")

def decode_http_header():
    key = load_key()
    print("Decoding HTTP header...")
    # Simulate retrieving headers (in real cases, you'd capture an actual HTTP response)
    encrypted_header_data = "gAAAAABnM5E-I_8ZihO1azvMLDcSL8RCyWYAS0tqjrvfAeOf0JrhoAPgEbDNJ-M8kFUv9mhwwljjCHqXRaiFLWQOzkS-_EgN2A=="  # Example encrypted data
    print(f"Captured HTTP Header with data: {encrypted_header_data}")
    decrypted_data = decrypt_data(encrypted_header_data.encode(), key)
    if decrypted_data:
        print("Decoded Data from HTTP header:", decrypted_data)
        decoded_data_list.append(decrypted_data)
    else:
        print("No valid encrypted data found in HTTP header.")

# Decode the data from a DNS query
def decode_dns_query():
    key = load_key()
    print("Decoding DNS query...")
    # Simulate capturing a DNS query (in real cases, you'd capture actual DNS responses)
    dns_encrypted_data = "gAAAAABnM5E-I_8ZihO1azvMLDcSL8RCyWYAS0tqjrvfAeOf0JrhoAPgEbDNJ-M8kFUv9mhwwljjCHqXRaiFLWQOzkS-_EgN2A=="  # Example encrypted data
    print(f"Captured DNS Query with data: {dns_encrypted_data}")
    decrypted_data = decrypt_data(dns_encrypted_data.encode(), key)
    if decrypted_data:
        print("Decoded Data from DNS query:", decrypted_data)
        decoded_data_list.append(decrypted_data)
    else:
        print("No valid encrypted data found in DNS query.")

# Function to get the decoded data
def get_decoded_data():
    key = load_key()
    print("Decoding all captured data...")
    
    with open('savedData.json', 'r') as file:
        data = json.load(file)
        
    print("Original Data:", data.get('inputData', ''))
    log_message(f"Original Data: {data.get('inputData', '')}")
    
    for encrypted_data in decoded_data_list:
        decrypted_data = decrypt_data(encrypted_data.encode(), key)
        if decrypted_data:
            print("Decoded Data:", decrypted_data)
        else:
            print("Failed to decode data:", encrypted_data)
    return decoded_data_list

# Main function to start the decoding process
def start_decoding():
    print("Starting decoding process...\n")
    decode_tcp_packet()
    decode_http_header()
    decode_dns_query()
    get_decoded_data()
    print("Decoding process complete.")

if __name__ == "__main__":
    start_decoding()