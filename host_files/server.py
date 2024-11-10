# /host_files/server.py
from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
import os

app = Flask(__name__)
CORS(app)

# Load CSV data
residents_data = pd.read_csv(os.path.join(os.getcwd(), 'host_files', 'residents.csv'))

@app.route("/getResidents", methods=["GET"])
def get_residents():
    data = residents_data.to_dict(orient="records")
    return jsonify(data)

@app.route("/searchResident", methods=["GET"])
def search_resident():
    name = request.args.get("name", "").lower()
    filtered_data = residents_data[residents_data["Name"].str.lower().str.contains(name)]
    return jsonify(filtered_data.to_dict(orient="records"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=2400)
