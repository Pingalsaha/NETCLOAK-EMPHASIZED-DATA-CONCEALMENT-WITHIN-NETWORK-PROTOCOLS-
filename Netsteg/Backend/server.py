from flask import Flask, request, jsonify
from flask_cors import CORS
from embed_module import start_embedding
from decrypt_module import start_decryption
from decode_module import start_decoding

import os
import json
import threading
import time
from datetime import datetime

app = Flask(__name__)
CORS(app)

SAVE_PATH = 'savedData.json'

# Read saved data from file
def read_saved_data():
    if os.path.exists(SAVE_PATH):
        with open(SAVE_PATH, 'r') as f:
            return json.load(f)
    return {}

# Write updated data back to file
def write_saved_data(data):
    with open(SAVE_PATH, 'w') as f:
        json.dump(data, f, indent=2)

# Append a new log entry
def log_message(msg):
    data = read_saved_data()
    if "logs" not in data:
        data["logs"] = []

    timestamp = datetime.utcnow().isoformat()
    log_entry = f"[{timestamp}] {msg}"
    data["logs"].insert(0, log_entry)
    write_saved_data(data)

# Processing thread that handles full cycle
def process_data(input_data):
    log_message("📤 Received input: " + input_data)

    # Step 1: Embed
    start_embedding(input_data)
    log_message("✅ Embedding completed.")

    # Step 2: Wait for traffic generation
    time.sleep(2)

    # Step 3: Decrypt captured packets
    start_decryption()
    log_message("🔓 Decryption completed.")

    # Step 4: Offline decode
    start_decoding()
    log_message("📂 Decoding (offline sync) completed.")

# API endpoint to receive user input
@app.route('/save-input', methods=['POST'])
def save_input():
    try:
        body = request.get_json()
        input_data = body.get("inputData", "")

        threading.Thread(target=process_data, args=(input_data,)).start()

        return jsonify({"message": "Data received. Processing started."}), 200
    except Exception as e:
        print(f"Error in /save-input: {e}")
        return jsonify({"message": "Error processing data"}), 500

# API to return logs
@app.route('/logs', methods=['GET'])
def get_logs():
    try:
        data = read_saved_data()
        return jsonify({"logs": data.get("logs", [])})
    except Exception as e:
        return jsonify({"logs": [], "error": str(e)}), 500

# API to return raw sniffed data
@app.route('/rawData', methods=['GET'])
def get_raw_data():
    try:
        data = read_saved_data()
        return jsonify({"rawData": data.get("rawData", [])})
    except Exception as e:
        return jsonify({"rawData": [], "error": str(e)}), 500

# API to return full history (used in Dashboard)
@app.route('/history', methods=['GET'])
def get_history():
    try:
        data = read_saved_data()
        history = data.get("history", [])
        sorted_history = sorted(history, key=lambda x: x["timestamp"], reverse=True)
        return jsonify({"history": sorted_history})
    except Exception as e:
        return jsonify({"history": [], "error": str(e)}), 500

# API to return only decrypted records (used in Receiver)
@app.route('/receive_data', methods=['GET'])
def receive_data():
    try:
        data = read_saved_data()
        history = data.get("history", [])
        decrypted_items = [
            {
                "input": item.get("input"),
                "encrypted": item.get("encrypted"),
                "decrypted": item.get("decrypted"),
                "protocol": item.get("protocol"),
                "timestamp": item.get("timestamp")
            }
            for item in history if item.get("decrypted")
        ]
        return jsonify(decrypted_items)
    except Exception as e:
        return jsonify({"received": [], "error": str(e)}), 500

# Start the Flask server
if __name__ == '__main__':
    print("🚀 Starting Flask server on port 5000...")
    app.run(port=5000)
