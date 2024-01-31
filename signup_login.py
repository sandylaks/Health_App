import sqlite3
import re
import anvil
import requests
from anvil.tables import app_tables
from kivy.lang import Builder
from kivy.uix.screenmanager import SlideTransition
from kivymd.app import MDApp
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.screen import MDScreen

Builder.load_file("signup.kv")
Builder.load_file("login.kv")

class Connection:
    def is_connected(self):
        try:
            # Attempt to make a simple HTTP request to check connectivity
            response = requests.get('https://www.google.com', timeout=5)
            response.raise_for_status()  # Raise an exception for HTTP errors
            return True
        except requests.RequestException:
            return False

    def get_database_connection(self):
        if self.is_connected():
            # Use Anvil's database connection
            return anvil.server.connect("server_5A3KARKYEQYWILR6V65KWJU2-YRPGRW5ZQBBQXWYJ")
        else:
            # Use SQLite database connection
            return sqlite3.connect('users.db')
class Signup(MDScreen,Connection):
    def users(self, instance, *args):

        username = self.ids.signup_username.text
        email = self.ids.signup_email.text
        password = self.ids.signup_password.text
        phone = self.ids.signup_phone.text
        pincode = self.ids.signup_pincode.text

        # Validation logic
        email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        # Enhanced password validation
        is_valid_password, password_error_message = self.validate_password(password)
        # Clear existing helper texts
        self.ids.signup_username.helper_text = ""
        self.ids.signup_email.helper_text = ""
        self.ids.signup_password.helper_text = ""
        self.ids.signup_phone.helper_text = ""
        self.ids.signup_pincode.helper_text = ""
        if not username:
            self.ids.signup_username.error = True
            self.ids.signup_username.helper_text = "Enter Name"
        elif not email or not re.match(email_regex, email):
            self.ids.signup_email.error = True
            self.ids.signup_email.helper_text = "Invalid Email"
        elif not is_valid_password:
            self.ids.signup_password.error = True
            self.ids.signup_password.helper_text = password_error_message
        elif not phone or len(phone) != 10:
            self.ids.signup_phone.error = True
            self.ids.signup_phone.helper_text = "Invalid Phone number (10 digits required)"
        elif not pincode or len(pincode) != 6:
            self.ids.signup_pincode.error = True
            self.ids.signup_pincode.helper_text = "Invalid Pincode (6 digits required)"

        else:
            # Clear any existing errors and helper texts
            self.ids.signup_username.error = False
            self.ids.signup_username.helper_text = ""
            self.ids.signup_email.error = False
            self.ids.signup_email.helper_text = ""
            self.ids.signup_password.error = False
            self.ids.signup_password.helper_text = ""
            self.ids.signup_phone.error = False
            self.ids.signup_phone.helper_text = ""
            self.ids.signup_pincode.error = False
            self.ids.signup_pincode.helper_text = ""

            #clear input texts
            self.ids.signup_username.text = ""
            self.ids.signup_email.text = ""
            self.ids.signup_password.text = ""
            self.ids.signup_phone.text = ""
            self.ids.signup_pincode.text = ""

            # If validation is successful, insert into the database
            try:
                if self.is_connected():
                    anvil.server.connect("server_5A3KARKYEQYWILR6V65KWJU2-YRPGRW5ZQBBQXWYJ")
                    rows = app_tables.users.search()
                    # Get the number of rows
                    id = len(rows) + 1
                    app_tables.users.add_row(
                        id=id,
                        username=username,
                        email=email,
                        password=password,
                        phone=float(phone),
                        pincode=int(pincode))
                    connection = sqlite3.connect('users.db')
                    cursor = connection.cursor()
                    cursor.execute('''
                                    INSERT INTO users (username, email, password, phone, pincode)
                                    VALUES (?, ?, ?, ?, ?)
                                ''', (username, email, password, phone, pincode))
                    connection.commit()
                    connection.close()
                else:
                    self.show_validation_dialog("No internet connection")

            except Exception as e:
                print(e)
                self.show_validation_dialog("No internet connection")
            # Navigate to the success screen
            app = MDApp.get_running_app()
            app.root.transition.direction = "left"
            app.root.current = "login"

    #password validation
    def validate_password(self, password):
        # Check if the password is not empty
        if not password:
            return False, "Password cannot be empty"
        # Check if the password has at least 8 characters
        if len(password) < 6:
            return False, "Password must have at least 6 characters"
        # Check if the password contains both uppercase and lowercase letters
        if not any(c.isupper() for c in password) or not any(c.islower() for c in password):
            return False, "Password must contain uppercase, lowercase"
        # Check if the password contains at least one digit
        if not any(c.isdigit() for c in password):
            return False, "Password must contain at least one digit"
        # Check if the password contains at least one special character
        special_characters = r"[!@#$%^&*(),.?\":{}|<>]"
        if not re.search(special_characters, password):
            return False, "Password must contain a special character"
        # All checks passed; the password is valid
        return True, "Password is valid"

    def show_validation_dialog(self, message):
        # Display a dialog for invalid login or sign up
        dialog = MDDialog(
            text=message,
            elevation=0,
            buttons=[MDFlatButton(text="OK", on_release=lambda x: dialog.dismiss())],
        )
        dialog.open()

class Login(MDScreen, Connection):
    def login_page(self, instance, *args):
        email = self.ids.login_email.text
        password = self.ids.login_password.text

        connection = self.get_database_connection()
        user_anvil = None
        user_sqlite = None
        try:
            if self.is_connected():
                # Fetch user from Anvil's database
                user_anvil = app_tables.users.get(
                    email=email,
                    password=password,
                )
            else:
                # Fetch user from SQLite database
                cursor = connection.cursor()
                cursor.execute('''
                            SELECT * FROM users
                            WHERE email = ? AND password = ?
                        ''', (email, password))
                user_sqlite = cursor.fetchone()
        finally:
            # Close the connection
            if connection and self.is_connected():
                connection.close()
        if user_anvil or user_sqlite:
            print("Login successful.")
            if user_anvil:
                username = str(user_anvil["username"])
                email = str(user_anvil["email"])
                phone = str(user_anvil["phone"])
                pincode = str(user_anvil["pincode"])
            elif user_sqlite:
                username = str(user_sqlite[1])
                email = str(user_sqlite[2])
                phone = str(user_sqlite[4])
                pincode = str(user_sqlite[5])
            app = MDApp.get_running_app()
            screen = app.root.get_screen('menu_profile')
            screen.ids.username.text = f"Username : {username}"
            screen.ids.email.text = f"Email : {email}"
            screen.ids.phone.text = f"Phone no : {phone}"
            screen.ids.pincode.text = f"Pincode : {pincode}"
            screen2 = app.root.get_screen('menu_profile_second')
            screen2.ids.username.text = f"Username : {username}"
            screen2.ids.email.text = f"Email : {email}"
            screen2.ids.phone.text = f"Phone no : {phone}"
            screen2.ids.pincode.text = f"Pincode : {pincode}"
            screen3 = app.root.get_screen('client_services')
            screen3.ids.username.text = username
            screen3.ids.email.text = email
            screen4 = app.root.get_screen('hospital_book')
            screen4.ids.username.text = username
            screen4.ids.email.text = email
            app.root.transition.direction = "left"
            app.root.current = "client_services"
        else:
            # Login failed
            self.ids.login_email.error = True
            self.ids.login_email.helper_text = "Invalid email or password"
            self.ids.login_password.error = True

