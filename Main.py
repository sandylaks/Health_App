import re

from kivy.lang import Builder
from kivymd import app
from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, SlideTransition
from kivy.core.text import LabelBase
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
import sqlite3

Window.size = (310, 580)

# SQLite database setup
conn = sqlite3.connect("users.db")  # Replace "users.db" with your desired database name
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        email TEXT NOT NULL,
        password TEXT NOT NULL,
        phone TEXT NOT NULL,
        pincode TEXT NOT NULL
    )
''')
conn.commit()


# Create the main app class
class LoginApp(MDApp):


    def validate_inputs(self, instance, *args):
        self.screen=Builder.load_file("signup.kv")
        screen = self.root.current_screen
        username = screen.ids.signup_username.text
        email = screen.ids.signup_email.text
        password = screen.ids.signup_password.text
        phone = screen.ids.signup_phone.text
        pincode = screen.ids.signup_pincode.text
        print(username)
        print(email)
        print(password)
        print(phone)
        print(pincode)

        # Validation logic
        email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not email or not re.match(email_regex, email):
            self.show_validation_dialog("Invalid Email")
        elif not password or len(password) < 6:
            self.show_validation_dialog("Invalid Password (at least 6 characters)")
        elif not pincode or len(pincode) != 6:
            self.show_validation_dialog("Invalid Pincode (6 digits required)")
        elif not phone or len(phone) != 10:
            self.show_validation_dialog("Invalid Phone number (10 digits required)")
        else:
            #If validation is successful, insert into the database
            cursor.execute('''
                        INSERT INTO users (username, email, password, phone, pincode)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (username, email, password, phone, pincode))
            conn.commit()
            # Navigate to the success screen
            self.root.transition = SlideTransition(direction='left')
            self.root.current = 'login'
    #
    def login(self,  instance, *args):
        self.screen1 = Builder.load_file("login.kv")
        screen1 = self.root.current_screen
        login_email = screen1.ids.login_email.text
        login_password = screen1.ids.login_password.text
        # Check if the user exists in the database for login
        cursor.execute('''
            SELECT * FROM users
            WHERE email = ? AND password = ?
        ''', (login_email, login_password))
        user = cursor.fetchone()

        if user:
            # Login successful
            print("Login successful. User details:", user)
            self.root.transition.direction = 'left'
            self.root.current = 'client_services'
        else:
            # Login failed
            self.show_validation_dialog("Invalid email or password")

    def show_validation_dialog(self, message):
        dialog = MDDialog(
            text=message,
            buttons=[MDFlatButton(text="OK", on_release=lambda x: dialog.dismiss())],
        )
        dialog.open()

    def build(self):
        screen_manager = ScreenManager()
        screen_manager.add_widget(Builder.load_file("main_sc.kv"))
        screen_manager.add_widget(Builder.load_file("login.kv"))
        screen_manager.add_widget(Builder.load_file("signup.kv"))
        screen_manager.add_widget(Builder.load_file("client_services.kv"))
        screen_manager.add_widget(Builder.load_file("menu_profile.kv"))
        screen_manager.add_widget(Builder.load_file("hospital_book.kv"))
        screen_manager.add_widget(Builder.load_file("service_provider.kv"))
        screen_manager.add_widget(Builder.load_file("service_register_form.kv"))



        return screen_manager


# Run the app
if __name__ == '__main__':
    LoginApp().run()
