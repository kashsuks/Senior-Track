from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd

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

@app.route("/getResidentData", methods=["GET"])
def get_resident_data():
    name = request.args.get("name", "").lower()
    resident = residents_data[residents_data["Name"].str.lower() == name]
    if not resident.empty:
        return jsonify(resident.iloc[0].to_dict())
    else:
        return jsonify({"error": "Resident not found"}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=2400)  # Set host and port for LAN access
