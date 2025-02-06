import sys
import sqlite3
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QDesktopWidget
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

from basic_client import start_client
# Database setup
def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (username TEXT PRIMARY KEY, password TEXT)''')
    conn.commit()
    conn.close()

# Login window
class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")

        # Get the screen dimensions
        screen = QDesktopWidget().screenGeometry()
        width = screen.width() // 2
        height = screen.height() // 2

        # Set the window size to half the screen
        self.setGeometry(100, 100, width, height)

        # Set stylesheet for a modern look
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2E3440;
            }
            QLabel {
                color: #D8DEE9;
                font-size: 16px;
            }
            QLineEdit {
                background-color: #4C566A;
                color: #D8DEE9;
                border: 1px solid #5E81AC;
                border-radius: 5px;
                padding: 10px;
                font-size: 14px;
            }
            QPushButton {
                background-color: #5E81AC;
                color: #ECEFF4;
                border: none;
                border-radius: 5px;
                padding: 15px;
                font-size: 16px;
                min-width: 150px;
            }
            QPushButton:hover {
                background-color: #81A1C1;
            }
        """)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()

        # Logo
        self.label_header = QLabel()
        self.label_header.setAlignment(Qt.AlignCenter)
        # Upscale the logo to fit better in the window
        self.label_header.setPixmap(QPixmap("D:\\newshell\\logo_resized.png").scaled(width // 2, height // 3, Qt.KeepAspectRatio))
        self.layout.addWidget(self.label_header)

        # Spacer
        self.layout.addSpacing(20)

        # Username field
        self.label_username = QLabel("Username:")
        self.layout.addWidget(self.label_username)

        self.entry_username = QLineEdit()
        self.entry_username.setPlaceholderText("Enter your username")
        self.layout.addWidget(self.entry_username)

        # Password field
        self.label_password = QLabel("Password:")
        self.layout.addWidget(self.label_password)

        self.entry_password = QLineEdit()
        self.entry_password.setPlaceholderText("Enter your password")
        self.entry_password.setEchoMode(QLineEdit.Password)
        self.layout.addWidget(self.entry_password)

        # Spacer
        self.layout.addSpacing(20)

        # Login button
        self.button_login = QPushButton("Login")
        self.button_login.clicked.connect(self.login)
        self.layout.addWidget(self.button_login)

        # Signup button
        self.button_signup = QPushButton("Sign Up")
        self.button_signup.clicked.connect(self.signup)
        self.layout.addWidget(self.button_signup)

        self.central_widget.setLayout(self.layout)

    def login(self):
        username = self.entry_username.text()
        password = self.entry_password.text()

        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        if c.fetchone():
            QMessageBox.information(self, "Login", "Login Successful")
            self.close()
            self.screen_share_window = ScreenShareWindow()
            self.screen_share_window.show()
        else:
            QMessageBox.critical(self, "Login", "Invalid Credentials")

    def signup(self):
        username = self.entry_username.text()
        password = self.entry_password.text()

        if not username or not password:
            QMessageBox.warning(self, "Sign Up", "Username and password cannot be empty")
            return

        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        try:
            c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            QMessageBox.information(self, "Sign Up", "Sign Up Successful")
        except sqlite3.IntegrityError:
            QMessageBox.critical(self, "Sign Up", "Username already exists")
        finally:
            conn.close()

# Screen sharing window
class ScreenShareWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Screen Sharing")
        self.setGeometry(100, 100, 800, 600)

        # Set stylesheet for a modern look
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2E3440;
            }
            QLabel {
                color: #D8DEE9;
                font-size: 16px;
            }
            QPushButton {
                background-color: #5E81AC;
                color: #ECEFF4;
                border: none;
                border-radius: 5px;
                padding: 15px;
                font-size: 16px;
                min-width: 150px;
            }
            QPushButton:hover {
                background-color: #81A1C1;
            }
        """)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()

        # Screen display label
        self.label_screen = QLabel("Waiting for screen...")
        self.label_screen.setAlignment(Qt.AlignCenter)
        self.label_screen.setStyleSheet("font-size: 18px; color: #88C0D0;")
        self.layout.addWidget(self.label_screen)

        # Start button
        self.button_start = QPushButton("Start Receiving Screen")
        self.button_start.clicked.connect(self.start_receiving)
        self.layout.addWidget(self.button_start)

        self.central_widget.setLayout(self.layout)

    def start_receiving(self):
        # Placeholder for networking functionality
        if started==False:
            print("Start receiving screen...")
            start_client()
            started=True
        else:
            print("already started")
        # threading.Thread(target=self.receive_screen, daemon=True).start()

    def receive_screen(self):
        # Placeholder for networking functionality
        pass

# Main application
if __name__ == "__main__":
    init_db()
    app = QApplication(sys.argv)
    login_window = LoginWindow()
    login_window.show()
    sys.exit(app.exec_())