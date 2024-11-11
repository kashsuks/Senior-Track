import tkinter as tk
from tkinter import messagebox
from tkinter.ttk import Entry, Button
import requests

SERVER_URL = "http://10.0.0.23:2400"

# Dummy Credentials
USERNAME = "admin"
PASSWORD = "123456"

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Senior Track System")
        self.root.geometry("500x400")

        # Initialize frames
        self.login_frame = tk.Frame(root)
        self.home_frame = tk.Frame(root)
        self.residents_frame = tk.Frame(root)

        # Build each frame
        self.build_login_frame()
        self.build_home_frame()
        self.build_residents_frame()

        # Start with login frame
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

        if username == USERNAME and password == PASSWORD:
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

        self.add_home_button(self.home_frame)

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

        self.data_label = tk.Label(self.residents_frame, text="", justify="left")
        self.data_label.pack(pady=20)

        self.add_home_button(self.residents_frame)

    def add_home_button(self, frame):
        home_button = tk.Button(frame, text="Home", command=lambda: self.show_frame(self.home_frame))
        home_button.pack(anchor="nw", padx=10, pady=10)

    def fetch_resident_suggestions(self, event):
        query = self.search_entry.get()
        if len(query) < 1:
            return

        try:
            response = requests.get(f"{SERVER_URL}/searchResident", params={"name": query})
            if response.status_code == 200:
                suggestions = response.json()
                self.update_suggestion_list([resident["Name"] for resident in suggestions])
            else:
                print(f"Error: {response.status_code}, {response.text}")
                messagebox.showerror("Error", "Failed to fetch residents")
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            messagebox.showerror("Error", "Failed to fetch residents")

    def update_suggestion_list(self, suggestions):
        self.suggestion_listbox.delete(0, tk.END)
        for name in suggestions:
            self.suggestion_listbox.insert(tk.END, name)

    def display_resident_data(self, event):
        selected_index = self.suggestion_listbox.curselection()
        if not selected_index:
            return

        name = self.suggestion_listbox.get(selected_index[0])
        try:
            response = requests.get(f"{SERVER_URL}/getResidentData", params={"name": name})
            if response.status_code == 200:
                resident_data = response.json()
                formatted_data = "\n".join([f"{key}: {value}" for key, value in resident_data.items()])
                self.data_label.config(text=formatted_data)
            else:
                messagebox.showerror("Error", "Failed to fetch resident data")
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            messagebox.showerror("Error", "Failed to fetch resident data")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()