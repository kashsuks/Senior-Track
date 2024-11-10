import tkinter as tk
from tkinter import ttk
from sv_ttk import ttk as svttk
import pandas as pd

residentData = pd.read_csv("residents.csv")

def checkLogin(username, password):
    if username == "admin" and password == "123456":
        return True
    return False

def createMainWindow():
    root = tk.Tk()
    root.title("Retirement Home Data Logger")
    root.geometry("800x600")
    svttk.set_theme("dark")

    loginFrame = tk.Frame(root)
    loginFrame.pack(pady=100)

    usernameLabel = svttk.Label(loginFrame, text="Username")
    usernameLabel.grid(row=0, column=0, padx=10, pady=5)
    usernameEntry = svttk.Entry(loginFrame)
    usernameEntry.grid(row=0, column=1, padx=10, pady=5)

    passwordLabel = svttk.Label(loginFrame, text="Password")
    passwordLabel.grid(row=1, column=0, padx=10, pady=5)
    passwordEntry = svttk.Entry(loginFrame, show="*")
    passwordEntry.grid(row=1, column=1, padx=10, pady=5)

    def loginAction():
        if checkLogin(usernameEntry.get(), passwordEntry.get()):
            loginFrame.destroy()
            createDashboard(root)
        else:
            errorLabel.config(text="Invalid username or password", foreground="red")
    
    loginButton = svttk.Button(loginFrame, text="Login", command=loginAction)
    loginButton.grid(row=2, column=0, columnspan=2, pady=10)

    errorLabel = svttk.Label(loginFrame, text="")
    errorLabel.grid(row=3, column=0, columnspan=2)

    root.mainloop()

def createDashboard(root):
    dashboardFrame = tk.Frame(root)
    dashboardFrame.pack(fill="both", expand=True)

    leftFrame = tk.Frame(dashboardFrame, width=200, bg="lightgray")
    leftFrame.pack(side="left", fill="y")

    residentsButton = svttk.Button(leftFrame, text="Residents", command=lambda: showResidents(dashboardFrame))
    residentsButton.pack(fill="x", pady=10)

    mealsButton = svttk.Button(leftFrame, text="Meals", command=mealPlaceholder)
    mealsButton.pack(fill="x", pady=10)

    welcomeLabel = svttk.Label(dashboardFrame, text="Welcome to the Retirement Home Data Logger", font=("Arial", 16))
    welcomeLabel.pack(pady=20)

def showResidents(dashboardFrame):
    for widget in dashboardFrame.winfo_children():
        widget.destroy()

    searchLabel = svttk.Label(dashboardFrame, text="Search Resident by Name", font=("Arial", 14))
    searchLabel.pack(pady=10)

    searchEntry = svttk.Entry(dashboardFrame, width=40)
    searchEntry.pack(pady=10)

    suggestionsListbox = tk.Listbox(dashboardFrame, width=40, height=5)
    suggestionsListbox.pack(pady=10)

    def updateSuggestions(event):
        searchTerm = searchEntry.get().lower()
        suggestionsListbox.delete(0, tk.END)
        for name in residentData["Name"]:
            if searchTerm in name.lower():
                suggestionsListbox.insert(tk.END, name)

    searchEntry.bind("<KeyRelease>", updateSuggestions)

    def displayResidentInfo():
        selectedResidentName = suggestionsListbox.get(tk.ACTIVE)
        if selectedResidentName:
            residentInfo = residentData[residentData["Name"] == selectedResidentName].iloc[0]
            showResidentInfo(dashboardFrame, residentInfo)

    suggestionsListbox.bind("<Double-1>", lambda e: displayResidentInfo())

def showResidentInfo(dashboardFrame, residentInfo):
    infoFrame = tk.Frame(dashboardFrame)
    infoFrame.pack(pady=20)

    nameLabel = svttk.Label(infoFrame, text=f"Name: {residentInfo['Name']}", font=("Arial", 12))
    nameLabel.pack(anchor="w")

    ageLabel = svttk.Label(infoFrame, text=f"Age: {residentInfo['Age']}", font=("Arial", 12))
    ageLabel.pack(anchor="w")

    dobLabel = svttk.Label(infoFrame, text=f"DOB: {residentInfo['DOB']}", font=("Arial", 12))
    dobLabel.pack(anchor="w")

    dietaryLabel = svttk.Label(infoFrame, text=f"Dietary Restrictions: {residentInfo['Dietary Restrictions']}", font=("Arial", 12))
    dietaryLabel.pack(anchor="w")

    contactLabel = svttk.Label(infoFrame, text=f"Contact Info: {residentInfo['Contact Info']}", font=("Arial", 12))
    contactLabel.pack(anchor="w")

def mealPlaceholder():
    print("Calling Meal API...")

if __name__ == "__main__":
    createMainWindow()
