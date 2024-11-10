import tkinter as tk
from tkinter import ttk
import requests

# Base URL of the server
SERVER_URL = "http://10.0.0.23:2400"  # Replace <host_ip> with the server's IP address

def fetch_residents():
    response = requests.get(f"{SERVER_URL}/getResidents")
    if response.status_code == 200:
        return response.json()
    return []

def search_residents(name):
    response = requests.get(f"{SERVER_URL}/searchResident", params={"name": name})
    if response.status_code == 200:
        return response.json()
    return []

def display_residents(data):
    # Clear current listbox items
    residentListbox.delete(0, tk.END)
    for resident in data:
        residentListbox.insert(tk.END, resident["Name"])

def on_search():
    name = searchEntry.get()
    results = search_residents(name)
    display_residents(results)

# Set up Tkinter GUI
root = tk.Tk()
root.title("Retirement Home Data Viewer")
root.geometry("800x600")

searchLabel = ttk.Label(root, text="Search Resident by Name", font=("Arial", 14))
searchLabel.pack(pady=10)

searchEntry = ttk.Entry(root, width=40)
searchEntry.pack(pady=10)

searchButton = ttk.Button(root, text="Search", command=on_search)
searchButton.pack(pady=5)

residentListbox = tk.Listbox(root, width=50, height=10)
residentListbox.pack(pady=20)

# Fetch all residents on startup
all_residents = fetch_residents()
display_residents(all_residents)

root.mainloop()
