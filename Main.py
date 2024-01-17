import base64
import re
from ServiceProvider import ServiceRegister,ServiceProvider,ServiceRegisterAmbulance,ServiceRegisterGym,ServiceProviderMain
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
import anvil.server
from anvil.tables import app_tables
import anvil.tables.query as q
anvil.server.connect("server_42NNKDLPGUOK3E7FTS3LKXZR-2KOMXZYBNO22QB25")




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

    # def google_sign_in(self):
    #     # Set up the OAuth 2.0 client ID and client secret obtained from the Google Cloud Console
    #     client_id = "407290580474-3ffjk8s253pdlsffjlm9io86aejpcq0m.apps.googleusercontent.com"
    #     client_secret = "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"
    #     redirect_uri = "urn:ietf:wg:oauth:2.0:oob"
    #
    #     # Set up the Google OAuth flow
    #     flow = InstalledAppFlow.from_client_secrets_file(
    #         "client_secret.json",
    #         scopes=["https://www.googleapis.com/auth/userinfo.email"]
    #     )
    #
    #     # Get the authorization URL
    #     auth_url, _ = flow.authorization_url(prompt="select_account")
    #
    #     # Open a web browser to the authorization URL
    #     import webbrowser
    #     webbrowser.open(auth_url)
    #
    #     # Get the authorization code from the user
    #     authorization_code = input("Enter the authorization code: ")
    #
    #     # Exchange the authorization code for credentials
    #     credentials = flow.fetch_token(
    #         token_uri="https://oauth2.googleapis.com/token",
    #         authorization_response=authorization_code
    #     )
    #
    #     # Use the obtained credentials for further Google API requests
    #     # Example: print the user's email address
    #     user_email = Credentials(credentials).id_token["email"]
    #     print(f"User email: {user_email}")

    def users(self, instance, *args):
        self.screen=Builder.load_file("signup.kv")
        screen = self.root.current_screen
        username = screen.ids.signup_username.text
        email = screen.ids.signup_email.text
        password = screen.ids.signup_password.text
        phone = screen.ids.signup_phone.text
        pincode = screen.ids.signup_pincode.text
        # print(username)
        # print(email)
        # print(password)
        # print(phone)
        # print(pincode)
        rows = app_tables.users.search()
        # Get the number of rows
        id = len(rows)+1

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

            #clear input texts
            screen.ids.signup_username.text = ""
            screen.ids.signup_email.text = ""
            screen.ids.signup_password.text = ""
            screen.ids.signup_phone.text = ""
            screen.ids.signup_pincode.text = ""

            app_tables.users.add_row(
                id=id,
                username=username,
                email=email,
                password=password,
                phone=float(phone),
                pincode=int(pincode))
            # Navigate to the success screen
            self.root.transition = SlideTransition(direction='left')
            self.root.current = 'login'

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
        email = screen1.ids.login_email.text
        password = screen1.ids.login_password.text

        # phone = float()
        # pincode = float()
        # Check if the user exists in the database for login
        user = app_tables.users.get(
            email=email,
            password=password,
        )

        if user:
            # Login successful
            print("Login successful.")

            username = user['username']
            phone = str(user['phone'])
            pincode = str(user['pincode'])

            # self.update(login_email, username)
            self.screen = Builder.load_file("menu_profile.kv")
            screen = self.root.get_screen('menu_profile')
            screen.ids.username.text = f"Username : {username}"
            screen.ids.email.text = f"Email : {email}"
            screen.ids.phone.text = f"Phone no : {phone}"
            screen.ids.pincode.text = f"Pincode : {pincode}"
            self.screen = Builder.load_file("client_services.kv")
            screen2 = self.root.get_screen('client_services')
            screen2.ids.username.text = username
            screen2.ids.email.text = email
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

        screen_manager.add_widget(Builder.load_file("main_sc.kv"))
        screen_manager.add_widget(Builder.load_file("login.kv"))
        screen_manager.add_widget(Builder.load_file("signup.kv"))
        screen_manager.add_widget(Builder.load_file("client_services.kv"))
        screen_manager.add_widget(Builder.load_file("menu_profile.kv"))
        screen_manager.add_widget(Builder.load_file("menu_notification.kv"))
        screen_manager.add_widget(Builder.load_file("menu_bookings.kv"))
        screen_manager.add_widget(Builder.load_file("menu_reports.kv"))
        screen_manager.add_widget(Builder.load_file("menu_support.kv"))
        screen_manager.add_widget(Builder.load_file("hospital_book.kv"))
        screen_manager.add_widget(ServiceProvider("service_provider"))
        screen_manager.add_widget(ServiceRegister("service_register_form"))
        screen_manager.add_widget(Builder.load_file("slot_booking.kv"))
        screen_manager.add_widget(Builder.load_file("payment_page.kv"))
        screen_manager.add_widget(ServiceRegisterGym("gym_register_form"))
        screen_manager.add_widget(ServiceRegisterAmbulance("ambulance_register_form"))
        screen_manager.add_widget(ServiceProviderMain(name="service_provider_main_page"))

        return screen_manager

    def show_customer_support_dialog(self):
        dialog = MDDialog(
            title="Contact Customer Support",
            text="Call Customer Support at: +1-800-123-4567"
        )
        dialog.open()

    def show_doctor_dialog(self):
        dialog = MDDialog(
            title="Call On-Call Doctor",
            text="Call On-Call Doctor at: +1-888-765-4321"
        )
        dialog.open()

    def submit_ticket(self):
        self.screen = Builder.load_file("menu_support.kv")
        screen = self.root.current_screen
        title = screen.ids.issue_title.text
        description = screen.ids.issue_description.text

        # if not title or not description:
        #     screen.ids.issue_title.error = "Please fill in all fields."
        #     return

        # Perform ticket submission logic here
        print(f"Ticket submitted:\nTitle: {title}\nDescription: {description}")

    def clear_text_input(self):
        self.screen = Builder.load_file("menu_support.kv")
        screen = self.root.current_screen
        screen.ids.issue_title.text = ''
        screen.ids.issue_description.text = ''

    def show_ticket_popup(self):
        self.screen = Builder.load_file("menu_support.kv")
        screen = self.root.current_screen
        submitted_text = screen.ids.issue_title.text

        # Create and show the popup
        ticket_popup = MDDialog(
            title="Ticket Raised",
            text=f"Ticket with content '{submitted_text}' has been raised.",
            buttons=[
                MDFlatButton(
                    text="OK",
                    md_bg_color=(1, 0, 0, 1),
                    theme_text_color="Custom",  # Use custom text color
                    text_color=(1, 1, 1, 1),  # White text color
                    font_size="13sp",  # Set the font size
                    on_release=lambda *args: ticket_popup.dismiss()
                ),
            ],
        )
        ticket_popup.open()
        screen.ids.issue_title.text = ''
        screen.ids.issue_description.text = ''
    #dialog box
    def show_validation_dialog(self, message):
        # Display a dialog for invalid login or sign up
        dialog = MDDialog(
            text=message,
            buttons=[MDFlatButton(text="OK", on_release=lambda x: dialog.dismiss())],
        )
        dialog.open()

    #-------------------------service-provider-flow-------------
    menu = None
    def open_dropdown(self):
        self.screen_service = Builder.load_file('service_register_form.kv')
        screen_service = self.root.current_screen
        if not self.menu:
            # Dropdown items (Replace these with your city names)
            cities = ["India",
                      "America",
                      "Russia",
                      "China"]
            items = [
                {
                    "viewclass": "MDDropDownItem",
                    "text": city,
                    "callback": self.select_city,
                } for city in cities
            ]
            self.menu = MDDropdownMenu(items=items, width_mult=3,max_height=300, pos_hint={'center_x': 0.5, 'center_y': 3})

        # Open the dropdown menu
        self.menu.caller = self.screen_service.ids.dropdown_nation
        self.menu.open()

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
        self.screen = Builder.load_file("service_register_form.kv")
        screen_hos_cancel = self.root.current_screen
        #screen_hos_cancel.ids.hospital_year.text = "You Clicked Cancel"

    def show_date_picker(self,arg):
        date_dialog = MDDatePicker( size_hint=(None, None), size=(150, 150))
        date_dialog.bind(on_save=self.on_save, on_cancel=self.on_cancel)
        date_dialog.open()

    def registration_submit(self):
        self.screen = Builder.load_file("service_register_form.kv")
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
        self.root.transition = SlideTransition(direction='right')
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
    LabelBase.register(name="OpenSans", fn_regular="fonts/Roboto-Regular.ttf")
    LoginApp().run()
