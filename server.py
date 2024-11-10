# server.py
from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
import os
import signal
import psutil

app = Flask(__name__)
CORS(app)

# Load CSV data
residents_data = pd.read_csv("residents.csv")

@app.route("/getResidents", methods=["GET"])
def get_residents():
    data = residents_data.to_dict(orient="records")
    return jsonify(data)

@app.route("/searchResident", methods=["GET"])
def search_resident():
    name = request.args.get("name", "").lower()
    filtered_data = residents_data[residents_data["Name"].str.lower().str.contains(name)]
    return jsonify(filtered_data.to_dict(orient="records"))

def kill_existing_process_on_port(port=2400):
    """Kill process using port 2400."""
    for proc in psutil.process_iter(attrs=["pid", "connections"]):
        for conn in proc.info.get("connections", []):
            if conn.laddr.port == port:
                print(f"Killing process {proc.info['pid']} using port {port}")
                proc.kill()

if __name__ == "__main__":
    # Ensure no server is already using the port
    kill_existing_process_on_port(2400)
    app.run(host="0.0.0.0", port=2400, use_reloader=False)  # Set host and port for LAN access
