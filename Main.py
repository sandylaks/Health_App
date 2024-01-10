import base64
import re
from ServiceProvider import ServiceRegister,ServiceProvider,ServiceRegisterAmbulance,ServiceRegisterGym


from kivymd.uix.pickers import MDDatePicker
# from kivyauth.google_auth import initialize_google,login_google,logout_google
from kivy.lang import Builder
from kivymd import app
from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, SlideTransition, Screen
from kivy.core.text import LabelBase
from kivymd.uix.behaviors import FakeRectangularElevationBehavior
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.pickers import MDDatePicker
from datetime import datetime
from kivy.uix.popup import Popup
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget



import sqlite3
from kivymd.uix.floatlayout import MDFloatLayout


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
# Create the BookSlot table if it doesn't exist

cursor.execute('''
    CREATE TABLE IF NOT EXISTS BookSlot (
        slot_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        username TEXT NOT NULL,
        book_date TEXT NOT NULL,
        book_time TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
''')

conn.commit()



class ProfileCard(MDFloatLayout, FakeRectangularElevationBehavior):
    pass

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
        # Enhanced password validation
        is_valid_password, password_error_message = self.validate_password(password)
        # Clear existing helper texts
        screen.ids.signup_email.helper_text = ""
        screen.ids.signup_password.helper_text = ""
        screen.ids.signup_phone.helper_text = ""
        screen.ids.signup_pincode.helper_text = ""

        if not email or not re.match(email_regex, email):
            screen.ids.signup_email.error = True
            screen.ids.signup_email.helper_text = "Invalid Email"
        elif not is_valid_password:
            screen.ids.signup_password.error = True
            screen.ids.signup_password.helper_text = password_error_message
        elif not phone or len(phone) != 10:
            screen.ids.signup_phone.error = True
            screen.ids.signup_phone.helper_text = "Invalid Phone number (10 digits required)"
        elif not pincode or len(pincode) != 6:
            screen.ids.signup_pincode.error = True
            screen.ids.signup_pincode.helper_text = "Invalid Pincode (6 digits required)"

        else:
            # Clear any existing errors and helper texts
            screen.ids.signup_email.error = False
            screen.ids.signup_email.helper_text = ""
            screen.ids.signup_password.error = False
            screen.ids.signup_password.helper_text = ""
            screen.ids.signup_phone.error = False
            screen.ids.signup_phone.helper_text = ""
            screen.ids.signup_pincode.error = False
            screen.ids.signup_pincode.helper_text = ""

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
    def login(self, instance, *args):
        self.screen1 = Builder.load_file("login.kv")


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

    def login_page(self,  instance, *args):
        self.screen = Builder.load_file("login.kv")

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
            username = user[1]
            # self.update(login_email, username)
            self.screen = Builder.load_file("menu_profile.kv")
            self.screen = Builder.load_file("client_services.kv")
            screen = self.root.get_screen('menu_profile')
            screen = self.root.get_screen('client_services')
            screen.ids.username.text = username
            screen.ids.email.text = login_email
            self.screen = Builder.load_file("client_services.kv")
            screen2 = self.root.get_screen('client_services')
            screen2.ids.username.text = username
            screen2.ids.email.text = login_email
            self.root.transition.direction = 'left'
            self.root.current = 'client_services'
        else:
            # Login failed
            self.screen = Builder.load_file("login.kv")
            screen1 = self.root.current_screen
            screen1.ids.login_email.error = True
            screen1.ids.login_email.helper_text = "Invalid email or password"
            screen1.ids.login_password.error = True


    def build(self):
        # client_id = open("client_id.txt")
        # client_secret = open("client_secret.txt")
        # initialize_google(self.after_login(), self.error_listener, client_id.read(),client_secret.read())
        screen_manager = ScreenManager()

        # screen_manager.add_widget(Builder.load_file("main_sc.kv"))
        # screen_manager.add_widget(Builder.load_file("login.kv"))
        # screen_manager.add_widget(Builder.load_file("signup.kv"))
        # screen_manager.add_widget(Builder.load_file("client_services.kv"))
        # screen_manager.add_widget(Builder.load_file("menu_profile.kv"))
        # screen_manager.add_widget(Builder.load_file("menu_notification.kv"))
        # screen_manager.add_widget(Builder.load_file("menu_bookings.kv"))
        # screen_manager.add_widget(Builder.load_file("menu_reports.kv"))
        # screen_manager.add_widget(Builder.load_file("menu_support.kv"))
        # screen_manager.add_widget(Builder.load_file("hospital_book.kv"))
        screen_manager.add_widget(ServiceProvider("service_provider"))
        screen_manager.add_widget(ServiceRegister("service_register_form"))
        screen_manager.add_widget(Builder.load_file("slot_booking.kv"))
        screen_manager.add_widget(ServiceRegisterGym("gym_register_form"))
        screen_manager.add_widget(ServiceRegisterAmbulance("ambulance_register_form"))
        screen_manager.add_widget(Builder.load_file("service_provider_main_page.kv"))

        return screen_manager


    def select_city(self, instance,instance_item):
        # Callback function when a city is selected
        selected_city = instance_item.text
        print(instance)
        # self.root.ids.dropdown_nation.text = selected_city
        # self.menu.dismiss()

    def on_save(self, instance, value, date_range):
        print(value)
        print(date_range)
        self.screen = Builder.load_file("hospital_book.kv")
        screen_hos = self.root.current_screen
        screen_hos.ids.dummy_widget.text = str(value)
        #self.show_date_dialog(value)

    # click Cancel
    def on_cancel(self, instance, value):
        print("cancel")
        self.screen = Builder.load_file("hospital_register_form.kv")
        screen_hos_cancel = self.root.current_screen
        #screen_hos_cancel.ids.hospital_year.text = "You Clicked Cancel"

    def show_date_picker(self,arg):
        date_dialog = MDDatePicker( size_hint=(None, None), size=(150, 150))
        date_dialog.bind(on_save=self.on_save, on_cancel=self.on_cancel)
        date_dialog.open()

    def registration_submit(self):
        self.screen = Builder.load_file("hospital_register_form.kv")
        screen = self.root.current_screen
        username = screen.ids.name.text
        print(username)
        # cursor.execute('''
        #     CREATE TABLE IF NOT EXISTS registration_forms (
        #         id INTEGER PRIMARY KEY AUTOINCREMENT,
        #         user_id INTEGER,
        #         name TEXT NOT NULL,
        #         email TEXT NOT NULL,
        #         password TEXT NOT NULL,
        #         address TEXT NOT NULL,
        #         nation TEXT NOT NULL,
        #         state TEXT NOT NULL,
        #         pin_code INTEGER NOT NULL,
        #         hospital_name TEXT NOT NULL,
        #         established_year TEXT NOT NULL,
        #         uploaded_documents BLOB,  -- New column for uploaded documents as BLOB
        #         UNIQUE (email)
        #     )
        # ''')
        # conn.commit()
        # # # Assuming file_data contains binary data of the file you want to upload
        # # file_data = b"..."
        # #
        # # # Encode the file data to base64 before inserting it into the database
        # # encoded_file_data = base64.b64encode(file_data)
        # cursor.execute('''
        #     INSERT INTO registration_forms (
        #         user_id, name, email, password, address, nation, state,
        #         pin_code, hospital_name, established_year, uploaded_documents
        #     )
        #     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        # ''', (user_id, name, email, password, address, nation, state, pin_code, hospital_name, established_year,
        #       encoded_file_data))

        conn.commit()

    # hospital_Book page logic
    # functionality for back button in hospital book
    def back_button_hospital_book(self):
        self.root.transition = SlideTransition(direction='left')
        self.root.current = 'client_services'


    # Slot_Booking page logic
    def slot_save(self, instance, value, date_range):
        # the date string in "year-month-day" format
        # date_object = datetime.strptime(str(value), "%Y-%m-%d")
        # Format the date as "day-month-year"
        # formatted_date = date_object.strftime("%d-%m-%Y")
        self.screen = Builder.load_file("slot_booking.kv")
        screen = self.root.current_screen
        book_date= str(value)
        # Retrieve book_time values for a specific book_date
        cursor.execute('''
                SELECT DISTINCT book_time
                FROM BookSlot
                WHERE book_date = ?
            ''', (book_date,))
        book_time_rows = cursor.fetchall()
        # Extract book_time values into a list
        book_times = [row[0] for row in book_time_rows]
        print(book_times)
        for date in book_times:
            print(date)
            screen.ids[date].disabled = True

        screen.ids.slot_date_label.text = str(value)
        screen.ids.session_date.text = str(value)


    def slot_cancel(self, instance, value):
        print("cancel")
        self.screen = Builder.load_file("slot_booking.kv")
        screen_hos_cancel = self.root.current_screen
        screen_hos_cancel.ids.slot_date_label.text = "You Clicked Cancel"
    def slot_date_picker(self):
        current_date = datetime.now().date()
        date_dialog = MDDatePicker(year=current_date.year, month=current_date.month, day=current_date.day, size_hint=(None, None), size=(150, 150))
        date_dialog.bind(on_save=self.slot_save, on_cancel=self.slot_cancel)
        date_dialog.open()

    def checkbox_click(self, checkbox, value, time):
        if value:
            self.screen = Builder.load_file("slot_booking.kv")
            screen = self.root.current_screen
            screen.ids.session_time.text = str(time)

    # Adding functionality to Pay now button
    def pay_now(self, instance, *args):
        self.screen = Builder.load_file("slot_booking.kv")
        screen = self.root.current_screen
        session_date = screen.ids.session_date.text
        session_time = screen.ids.session_time.text
        # Extract the username from menu_profile
        self.screen = Builder.load_file("menu_profile.kv")
        screen = self.root.get_screen('menu_profile')
        username = screen.ids.username.text
        print(username)
        # Retrieve all book_Date entries from BookSlot table
        cursor.execute('''
                    SELECT book_date FROM BookSlot
                ''')
        book_date_rows = cursor.fetchall()
        # Extract book_date values into a list
        book_dates = [row[0] for row in book_date_rows]
        # Retrieve all book_time entries from BookSlot table
        cursor.execute('''
            SELECT book_time FROM BookSlot
        ''')
        book_time_rows = cursor.fetchall()
        # Extract book_time values into a list
        book_times = [row[0] for row in book_time_rows]

        # Condition for pay now button
        if session_time in book_times and session_date in book_dates:
            self.show_validation_dialog(f'This {session_time}for {session_date} is already booked ')

        elif len(session_date) == 10 and len(session_time) >= 9 :
            cursor.execute('''
                                        SELECT id, username FROM users WHERE username = ?
                                    ''', (username,))
            user_row = cursor.fetchone()

            # If date and time are successfully Selected, insert into the database
            user_id, fetched_username = user_row
            # Insert a new booking into the BookSlot table
            cursor.execute('''
                       INSERT INTO BookSlot (user_id, username, book_date, book_time)
                       VALUES (?, ?, ?, ?)
                   ''', (user_id, fetched_username, session_date, session_time))

            conn.commit()
            self.root.transition.direction = 'left'
            self.root.current = 'payment_page'
        elif len(session_date) == 4 and len(session_time) >= 9 :
            self.show_validation_dialog("Select Date")
        elif len(session_date) == 10 and len(session_time) == 4:
            self.show_validation_dialog("Select Time")
        else:
            self.show_validation_dialog("Select Date and Time")

    # payment_page page logic
    # logic for back button in payment_page
    def payment_page_backButton(self):
        # Extract the username from menu_profile
        self.screen = Builder.load_file("menu_profile.kv")
        screen = self.root.get_screen('menu_profile')
        username = screen.ids.username.text
        print(username)
        # Execute the SQL DELETE statement
        cursor.execute("DELETE FROM BookSlot WHERE username = ?", (username,))
        # Commit the changes and close the connection
        conn.commit()


        self.root.transition = SlideTransition(direction='right')
        self.root.current = 'slot_booking'


# Run the app
if __name__ == '__main__':
    LabelBase.register(name="MPoppins", fn_regular="Poppins/Poppins-Medium.ttf")
    LabelBase.register(name="BPoppins", fn_regular="Poppins/Poppins-Bold.ttf")
    LoginApp().run()
