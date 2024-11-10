from flask import Flask, request, jsonify
import csv
from datetime import datetime, timedelta

app = Flask(__name__)
residentsCsv = "residents.csv"
mealsCsv = "meals.csv"

@app.route("/searchResident", methods=["GET"])
def searchResident():
    name = request.args.get("name")
    residentInfo = None
    with open(residentsCsv, mode="r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["name"].lower() == name.lower():
                residentInfo = row
                break
    if residentInfo:
        return jsonify({"status": "success", "data": residentInfo}), 200
    else:
        return jsonify({"status": "error", "message": "Resident not found"}), 404

@app.route("/searchMeals", methods=["GET"])
def searchMeals():
    mealType = request.args.get("mealType")
    day = request.args.get("day")  # Format: "YYYY-MM-DD"
    results = []

    # Validate date format
    try:
        targetDate = datetime.strptime(day, "%Y-%m-%d").date()
    except ValueError:
        return jsonify({"status": "error", "message": "Invalid date format"}), 400

    # Retrieve meal data from the past 30 days only
    startDate = targetDate - timedelta(days=30)
    with open(mealsCsv, mode="r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            mealDate = datetime.strptime(row["date"], "%Y-%m-%d").date()
            if startDate <= mealDate <= targetDate and row["mealType"].lower() == mealType.lower():
                results.append(row)

    if results:
        return jsonify({"status": "success", "data": results}), 200
    else:
        return jsonify({"status": "error", "message": "No meals found for specified day and meal type"}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=2400)
