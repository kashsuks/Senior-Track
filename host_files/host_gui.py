import tkinter as tk
from tkinter import messagebox
import requests
from flask import Flask, jsonify, request
from threading import Thread
import pandas as pd
import os
import sys

if getattr(sys, 'frozen', False):
    application_path = sys._MEIPASS
else:
    application_path = os.getcwd()

app = Flask(__name__)
csv_file_path = os.path.join(application_path, 'residents.csv')
residents_data = pd.read_csv(csv_file_path)

@app.route("/getResidents", methods=["GET"])
def get_residents():
    data = residents_data.to_dict(orient="records")
    return jsonify(data)

@app.route("/searchResident", methods=["GET"])
def search_resident():
    name = request.args.get("name", "").lower()
    filtered_data = residents_data[residents_data["Name"].str.lower().str.contains(name)]
    return jsonify(filtered_data.to_dict(orient="records"))

def run_server():
    app.run(host="0.0.0.0", port=2400, use_reloader=False)

class ClientApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Client Senior Track System")
        self.root.geometry("500x400")

        self.login_frame = tk.Frame(root)
        self.home_frame = tk.Frame(root)
        self.residents_frame = tk.Frame(root)

        self.build_login_frame()
        self.build_home_frame()
        self.build_residents_frame()

        self.show_frame(self.login_frame)

    def show_frame(self, frame):
        frame.tkraise()

    def build_login_frame(self):
        self.login_frame.place(relwidth=1, relheight=1)

        tk.Label(self.login_frame, text="Username").pack(pady=10)
        self.username_entry = tk.Entry(self.login_frame)
        self.username_entry.pack()

        tk.Label(self.login_frame, text="Password").pack(pady=10)
        self.password_entry = tk.Entry(self.login_frame, show="*")
        self.password_entry.pack()

        login_button = tk.Button(self.login_frame, text="Login", command=self.check_login)
        login_button.pack(pady=20)

    def check_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username == "admin" and password == "123456":
            self.show_frame(self.home_frame)
        else:
            messagebox.showerror("Error", "Invalid Username or Password")

    def build_home_frame(self):
        self.home_frame.place(relwidth=1, relheight=1)

        home_label = tk.Label(self.home_frame, text="Home Page", font=("Helvetica", 18))
        home_label.pack(pady=20)

        residents_button = tk.Button(self.home_frame, text="Residents", command=lambda: self.show_frame(self.residents_frame))
        residents_button.pack(pady=10)

        meals_button = tk.Button(self.home_frame, text="Meals")
        meals_button.pack(pady=10)

    def build_residents_frame(self):
        self.residents_frame.place(relwidth=1, relheight=1)

        search_label = tk.Label(self.residents_frame, text="Search Resident")
        search_label.pack(pady=10)

        self.search_entry = tk.Entry(self.residents_frame)
        self.search_entry.pack()
        self.search_entry.bind("<KeyRelease>", self.fetch_resident_suggestions)

        self.suggestion_listbox = tk.Listbox(self.residents_frame)
        self.suggestion_listbox.pack(pady=10)
        self.suggestion_listbox.bind("<<ListboxSelect>>", self.display_resident_data)

    def fetch_resident_suggestions(self, event):
        query = self.search_entry.get()
        if len(query) < 1:
            return

        try:
            response = requests.get(f"http://127.0.0.1:2400/searchResident", params={"name": query})
            if response.status_code == 200:
                suggestions = response.json()
                self.update_suggestion_list(suggestions)
            else:
                messagebox.showerror("Error", "Failed to fetch residents")
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"Request failed: {e}")

    def update_suggestion_list(self, suggestions):
        self.suggestion_listbox.delete(0, tk.END)
        for resident in suggestions:
            self.suggestion_listbox.insert(tk.END, resident["Name"])

    def display_resident_data(self, event):
        selected_index = self.suggestion_listbox.curselection()
        if not selected_index:
            return
        selected_resident = self.suggestion_listbox.get(selected_index)
        messagebox.showinfo("Resident Data", f"Selected Resident: {selected_resident}")

if __name__ == "__main__":
    server_thread = Thread(target=run_server)
    server_thread.daemon = True
    server_thread.start()

    root = tk.Tk()
    app = ClientApp(root)
    root.mainloop()
