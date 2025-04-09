import base64
import json
from cryptography.fernet import Fernet
import scapy.all as scapy
import dns.resolver
import requests
import os

# Log messages to JSON file
def log_rawData(message):
    file_path = 'savedData.json'
    try:
        # Read existing rawData if file exists
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                data = json.load(f)
        else:
            data = {}

        # Initialize rawData list if it doesn't exist
        if 'rawData' not in data:
            data['rawData'] = []

        # Append new message to rawData
        data['rawData'].append(message)

        # Write updated data back to file
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        print(f"Error logging message: {e}")

# Function to load the encryption key
def load_key():
    key_path = "secret.key"
    if os.path.exists(key_path):
        with open(key_path, "rb") as key_file:
            key = key_file.read()
        return key
    else:
        raise Exception("Encryption key not found. Please run embed_module.py to generate the key.")

# Decrypt data using the Fernet key
def decrypt_data(encrypted_data, key):
    cipher = Fernet(key)
    try:
        decrypted_data = cipher.decrypt(encrypted_data)
        return decrypted_data.decode()  # Decode bytes to string
    except Exception:
        return None  # Return None if decryption fails

# Capture TCP packets and try to extract embedded data
def capture_tcp_packets():
    key = load_key()
    print("Capturing TCP packets...")

    # Increase packet count and timeout
    packets = scapy.sniff(filter="tcp", timeout=30)  # Capture more packets over a longer time
    for packet in packets:
        try:
            if packet.haslayer(scapy.TCP) and packet.haslayer(scapy.Raw):
                raw_data = packet[scapy.Raw].load
                print(f"Captured TCP Packet with data: {raw_data}")
                log_rawData(raw_data.decode(errors='ignore'))
                decrypted_data = decrypt_data(raw_data, key)
                if decrypted_data:
                    print("Decrypted Data from TCP packet:", decrypted_data)
                    log_rawData(f"Decrypted Data from TCP packet: {decrypted_data.decode(errors='ignore')}")
                else:
                    print("No valid encrypted data found in this TCP packet.")
        except Exception as e:
            print(f"Error extracting data from TCP packet: {e}")


# Capture HTTP headers and extract embedded data from the User-Agent header
def capture_http_headers():
    key = load_key()
    url = "http://example.com"
    headers = {"User-Agent": "HiddenData123"}  # Send identifiable request for filtering
    try:
        response = requests.get(url, headers=headers)
        print("Captured HTTP Response Headers:", response.headers)
        
        # Retrieve the User-Agent header from our original request headers
        hidden_data = headers.get('User-Agent', '')
        decrypted_data = decrypt_data(hidden_data.encode(), key)
        
        if decrypted_data:
            print("Decrypted Data from HTTP header:", decrypted_data)
        else:
            print("No valid encrypted data found in HTTP header.")
    except Exception as e:
        print(f"Error capturing HTTP headers: {e}")


# Capture DNS queries and attempt to extract embedded data
def capture_dns_queries():
    key = load_key()
    resolver = dns.resolver.Resolver()
    try:
        query = resolver.query("HiddenData123.example.com", "A")
        print("Captured DNS query:", query)
        decrypted_data = decrypt_data(query[0].to_text().encode(), key)
        if decrypted_data:
            print("Decrypted Data from DNS query:", decrypted_data)
        else:
            print("No valid encrypted data found in DNS query.")
    except dns.resolver.NXDOMAIN:
        print("DNS query error: Domain does not exist.")
    except Exception as e:
        print(f"Error capturing DNS query: {e}")

# Main function to start decryption process
def start_decryption():
    print("Starting decryption process...")
    capture_tcp_packets()
    capture_http_headers()
    capture_dns_queries()
    print("Decryption process complete.")

if __name__ == "__main__":
    start_decryption()