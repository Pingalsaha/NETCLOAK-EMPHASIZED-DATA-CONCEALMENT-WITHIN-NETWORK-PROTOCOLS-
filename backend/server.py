from flask import Flask, request, jsonify  # type: ignore
from flask_cors import CORS  # type: ignore
from embed_module import start_embedding
from decrypt_module import start_decryption
from decode_module import start_decoding
import time
import json
import os
import threading

app = Flask(__name__)
CORS(app)

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

# Function to take user input from the saved JSON file
def get_input_data():
    with open('savedData.json', 'r') as file:
        data = json.load(file)
    return data.get('inputData', '')

# Function to execute embedding of data in TCP, HTTP, and DNS
def execute_embedding(data):
    log_message("Embedding data into TCP packets...")
    start_embedding()  # Calls the embedding process
    log_message("Embedding completed.")

# Function to execute decryption by sniffing network traffic
def execute_decryption():
    log_message("Starting packet sniffing and decryption...")
    start_decryption()  # Calls the decryption process
    log_message("Decryption completed.")

# Function to execute the decoding of encrypted data
def execute_decoding():
    log_message("Starting decoding process...")
    start_decoding()  # Calls the decoding process
    log_message("Decoding completed.")

# Combined function to run the embedding, decryption, and decoding process
def process_data():
    # Step 1: Get the data to hide
    data = get_input_data()
    
    # Step 2: Embed the data into different protocols (TCP, HTTP, DNS)
    execute_embedding(data)
    
    # Step 3: Simulate a delay before starting the decryption process
    time.sleep(1)  # Simulating network propagation delay
    
    # Step 4: Start sniffing and decrypting the embedded data
    execute_decryption()
    
    # Step 5: Decode the encrypted data from various protocols
    execute_decoding()

# Endpoint to save input data and trigger the data processing
@app.route('/save-input', methods=['POST'])
def save_input():
    data = request.get_json()  # Get the JSON data from the request
    file_path = os.path.join(os.path.dirname(__file__), 'savedData.json')
    
    try:
        # Save the data to savedData.json
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)
        log_message("Data saved successfully. Initiating data processing...")
        
        # Run the data processing in a separate thread to avoid blocking the server
        threading.Thread(target=process_data).start()
        
        return jsonify({"message": "Data saved and processing started"}), 200
    except Exception as e:
        print(f"Error saving data: {e}")
        return jsonify({"message": "Error saving data"}), 500

# Endpoint to fetch the logs from savedData.json
@app.route('/logs', methods=['GET'])
def get_logs():
    try:
        with open('savedData.json', 'r') as file:
            data = json.load(file)
        logs = data.get('logs', [])
        return jsonify({"logs": logs})
    except Exception as e:
        print(f"Error reading logs: {e}")
        return jsonify({"logs": [], "error": str(e)}), 500
    
    
# Endpoint to fetch the rawData from savedData.json
@app.route('/rawData', methods=['GET'])
def get_rawData():
    try:
        with open('savedData.json', 'r') as file:
            data = json.load(file)
        rawData = data.get('rawData', [])
        return jsonify({"rawData": rawData})
    except Exception as e:
        print(f"Error reading rawData: {e}")
        return jsonify({"rawData": [], "error": str(e)}), 500

if __name__ == '__main__':
    print("Starting the Flask server on port 5000...\n")
    app.run(port=5000)