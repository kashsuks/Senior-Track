import requests

serverUrl = "http://10.0.0.23:2400"

def searchResident(name):
    response = requests.get(f"{serverUrl}/searchResident", params={"name": name})
    if response.status_code == 200:
        print("Resident Info:", response.json()["data"])
    else:
        print(response.json()["message"])

def searchMeals(mealType, day):
    response = requests.get(f"{serverUrl}/searchMeals", params={"mealType": mealType, "day": day})
    if response.status_code == 200:
        print(f"{mealType.capitalize()} on {day}:")
        for record in response.json()["data"]:
            print(f"{record['residentName']}: {record['hadMeal']}")
    else:
        print(response.json()["message"])

# Example usage
searchResident("Jane Smith")
searchMeals("lunch", "2025-12-26")
