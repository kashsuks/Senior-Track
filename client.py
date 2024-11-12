import sys
import requests
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QListWidget, QMessageBox, QStackedWidget
import qdarktheme

SERVER_URL = "http://10.0.0.23:2400"
USERNAME = "admin"
PASSWORD = "123456"

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Senior Track System")
        self.setGeometry(100, 100, 500, 400)

        # Initialize the stacked widget to manage different screens
        self.stacked_widget = QStackedWidget(self)
        self.setCentralWidget(self.stacked_widget)

        self.build_login_frame()

    def build_login_frame(self):
        layout = QVBoxLayout()

        self.username_entry = QLineEdit(self)
        self.username_entry.setPlaceholderText("Username")

        self.password_entry = QLineEdit(self)
        self.password_entry.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_entry.setPlaceholderText("Password")

        login_button = QPushButton("Login", self)
        login_button.clicked.connect(self.check_login)

        layout.addWidget(QLabel("Login"))
        layout.addWidget(self.username_entry)
        layout.addWidget(self.password_entry)
        layout.addWidget(login_button)

        login_widget = QWidget(self)
        login_widget.setLayout(layout)

        # Add the login widget to the stacked widget
        self.stacked_widget.addWidget(login_widget)
        self.stacked_widget.setCurrentWidget(login_widget)

    def check_login(self):
        if self.username_entry.text() == USERNAME and self.password_entry.text() == PASSWORD:
            self.build_home_frame()
        else:
            QMessageBox.critical(self, "Error", "Invalid Username or Password")

    def build_home_frame(self):
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Home Page"))

        residents_button = QPushButton("Residents", self)
        residents_button.clicked.connect(self.build_residents_frame)
        layout.addWidget(residents_button)

        home_widget = QWidget(self)
        home_widget.setLayout(layout)

        # Switch to the home screen
        self.stacked_widget.addWidget(home_widget)
        self.stacked_widget.setCurrentWidget(home_widget)

    def build_residents_frame(self):
        layout = QVBoxLayout()

        self.search_entry = QLineEdit(self)
        self.search_entry.setPlaceholderText("Search Resident")
        self.search_entry.textChanged.connect(self.fetch_resident_suggestions)

        self.suggestion_listbox = QListWidget(self)
        self.suggestion_listbox.itemClicked.connect(self.display_resident_data)

        layout.addWidget(self.search_entry)
        layout.addWidget(self.suggestion_listbox)

        residents_widget = QWidget(self)
        residents_widget.setLayout(layout)

        # Switch to the residents screen
        self.stacked_widget.addWidget(residents_widget)
        self.stacked_widget.setCurrentWidget(residents_widget)

    def fetch_resident_suggestions(self):
        query = self.search_entry.text()
        if len(query) < 1:
            return
        try:
            response = requests.get(f"{SERVER_URL}/searchResident", params={"name": query})
            if response.status_code == 200:
                suggestions = response.json()
                self.update_suggestion_list([resident["Name"] for resident in suggestions])
            else:
                QMessageBox.critical(self, "Error", "Failed to fetch residents")
        except requests.exceptions.RequestException:
            QMessageBox.critical(self, "Error", "Failed to fetch residents")

    def update_suggestion_list(self, suggestions):
        self.suggestion_listbox.clear()
        self.suggestion_listbox.addItems(suggestions)

    def display_resident_data(self, item):
        name = item.text()
        try:
            response = requests.get(f"{SERVER_URL}/getResidentData", params={"name": name})
            if response.status_code == 200:
                resident_data = response.json()
                formatted_data = "\n".join([f"{key}: {value}" for key, value in resident_data.items()])
                QMessageBox.information(self, "Resident Data", formatted_data)
            else:
                QMessageBox.critical(self, "Error", "Failed to fetch resident data")
        except requests.exceptions.RequestException:
            QMessageBox.critical(self, "Error", "Failed to fetch resident data")

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Apply the dark theme using qdarktheme
    qdarktheme.setup_theme()

    main_win = App()
    main_win.show()
    sys.exit(app.exec())
