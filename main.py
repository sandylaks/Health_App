import base64
import json
import re
import webbrowser


from kivymd.uix.navigationdrawer import MDNavigationLayout
from signup_login import Signup, Login
from ServiceProvider import ServiceRegisterForm
from slot_booking import Slot_Booking
from ServiceProvider import ServiceProviderMain,ServiceProfile,ServiceNotification,ServiceSupport,ServiceSlotAdding

# from kivyauth.google_auth import initialize_google,login_google,logout_google
from ServiceProvider import ServiceRegister, ServiceProvider, ServiceRegisterAmbulance, ServiceRegisterGym, ServiceProviderMain


from kivy.lang import Builder
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
import requests

# from kivy.uix.webview import WebView
# from google_auth_oauthlib.flow import InstalledAppFlow
# import webbrowser
# from google.auth.credentials import Credentials

import razorpay
# from crosswalk import WebView
import sqlite3
from kivymd.uix.floatlayout import MDFloatLayout


Window.size = (320, 580)

# SQLite database setup
conn = sqlite3.connect("users.db")
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
class MDNavigationLayout(MDNavigationLayout):
    pass

# Create the main app class
class LoginApp(MDApp):

    # def google_sign_in(self):
    #     # Set up the OAuth 2.0 client ID and client secret obtained from the Google Cloud Console
    #     client_id = "749362207551-tdoq2d8787csqqnbvpdgcc3m2sdtsnd1.apps.googleusercontent.com"
    #     client_secret = "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"
    #     redirect_uri = "https://oxivive.com/oauth/callback"
    #     redirect_uri = "urn:ietf:wg:oauth:2.0:oob"
    #
    #     # Set up the Google OAuth flow
    #     flow = InstalledAppFlow.from_client_secrets_file(
    #         "client_secret.json",
    #         scopes=["https://www.googleapis.com/auth/userinfo.email"],
    #         redirect_uri=redirect_uri
    #     )
    #
    #     # Get the authorization URL
    #     auth_url, _ = flow.authorization_url(prompt="select_account")
    #     print(f"Authorization URL: {auth_url}")
    #
    #     # Open a web browser to the authorization URL
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
    #     user_email = credentials.id_token["email"]
    #     print(f"User email: {user_email}")
    #
    # def exchange_code_for_tokens(self, authorization_code):
    #     token_url = "https://oauth2.googleapis.com/token"
    #
    #     params = {
    #         "code": authorization_code,
    #         "client_id": "your_client_id",
    #         "client_secret": "your_client_secret",
    #         "redirect_uri": "urn:ietf:wg:oauth:2.0:oob",
    #         "grant_type": "authorization_code"
    #     }
    #
    #     response = requests.post(token_url, data=params)
    #     token_data = response.json()
    #
    #     return token_data

    def build(self):
        screen_manager = ScreenManager()

        screen_manager.add_widget(Builder.load_file("main_sc.kv"))
        screen_manager.add_widget(Login(name="login"))
        screen_manager.add_widget(Signup(name="signup"))
        screen_manager.add_widget(Builder.load_file("client_services.kv"))
        screen_manager.add_widget(Builder.load_file("client_services1.kv"))
        screen_manager.add_widget(Builder.load_file("menu_profile.kv"))
        screen_manager.add_widget(Builder.load_file("menu_notification.kv"))
        screen_manager.add_widget(Builder.load_file("menu_bookings.kv"))
        screen_manager.add_widget(Builder.load_file("menu_reports.kv"))
        screen_manager.add_widget(Builder.load_file("menu_support_second.kv"))
        screen_manager.add_widget(Builder.load_file("menu_profile_second.kv"))
        screen_manager.add_widget(Builder.load_file("menu_notification_second.kv"))
        screen_manager.add_widget(Builder.load_file("menu_bookings_second.kv"))
        screen_manager.add_widget(Builder.load_file("menu_reports_second.kv"))
        screen_manager.add_widget(Builder.load_file("menu_support.kv"))
        screen_manager.add_widget(Builder.load_file("hospital_book.kv"))
        screen_manager.add_widget(ServiceProvider("service_provider"))
        screen_manager.add_widget(ServiceRegister("service_register_form"))
        screen_manager.add_widget(Slot_Booking(name="slot_booking"))
        screen_manager.add_widget(Builder.load_file("payment_page.kv"))
        screen_manager.add_widget(ServiceRegisterGym("gym_register_form"))
        screen_manager.add_widget(ServiceRegisterAmbulance("ambulance_register_form"))
        screen_manager.add_widget(ServiceProviderMain(name="service_provider_main_page"))
        screen_manager.add_widget(ServiceProfile(name="service_profile"))
        screen_manager.add_widget(ServiceNotification(name="service_notification"))
        screen_manager.add_widget(ServiceSlotAdding(name="service_slot_adding"))
        screen_manager.add_widget(ServiceSupport(name="service_support"))
        screen_manager.add_widget(ServiceRegisterForm())

        return screen_manager
    def client_services1(self):
        self.root.transition.direction = 'left'
        self.root.current = 'client_services1'
    def fetch_pincode(self):
        self.screen = Builder.load_file("client_services1.kv")
        screen = self.root.current_screen
        pincode = screen.ids.pincode.text
        if not pincode or len(pincode) != 6:
            screen.ids.pincode.error = True
            screen.ids.pincode.helper_text = "Invalid Pincode (6 digits required)"
        else:
            screen.ids.pincode.error = False
            screen.ids.pincode.helper_text = ""
            screen.ids.pincode.text = ""
            self.root.transition.direction = 'left'
            self.root.current = 'client_services'
    def get_location(self):
        import json
        from urllib.request import urlopen

        url = 'http://ipinfo.io/json'
        response = urlopen(url)
        data = json.load(response)
        pincode = data["postal"]
        self.screen = Builder.load_file("client_services1.kv")
        screen = self.root.current_screen
        screen.ids.pincode.text = pincode

    def logout(self):
        self.root.transition.direction = 'left'
        self.root.current = 'login'

    def show_customer_support_dialog(self):
        dialog = MDDialog(
            title="Contact Customer Support",
            text="Call Customer Support at: +1-800-123-4567",
            elevation = 0
        )
        dialog.open()

    def show_doctor_dialog(self):
        dialog = MDDialog(
            title="Call On-Call Doctor",
            text="Call On-Call Doctor at: +1-888-765-4321",
            elevation=0
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
            elevation=0,
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
            elevation=0,
            buttons=[MDFlatButton(text="OK", on_release=lambda x: dialog.dismiss())],
        )
        dialog.open()

    def registration_submit(self):
        self.screen = Builder.load_file("service_register_form.kv")
        screen = self.root.current_screen
        username = screen.ids.name.text
        print(username)


    # hospital_Book page logic
    def back_button_hospital_book(self):
        self.root.transition = SlideTransition(direction='right')
        self.root.current = 'client_services'


    # Slot_Booking pagelogic

    # time_slots = ['9am - 11am', '11am - 1pm', '1pm - 3pm', '3pm - 5pm', '5pm - 7pm', '7pm - 9pm']
    # def slot_booking_back_button(self, instance):
    #     self.screen = Builder.load_file("slot_booking.kv")
    #     screen = self.root.current_screen
    #     screen.ids.date_choosed.text = "Choose a date"
    #     for slots in LoginApp.time_slots:
    #         screen.ids[slots].disabled = False
    #         screen.ids[slots].md_bg_color = (1, 1, 1, 1)
    #
    #     self.root.transition = SlideTransition(direction='right')
    #     self.root.current = 'hospital_book'
    # def select_timings(self, button, label_text):
    #     self.session_time = label_text
    #     print(self.session_time)
    #     self.screen = Builder.load_file("slot_booking.kv")
    #     screen = self.root.current_screen
    #     selected_slot = label_text
    #     for slot in LoginApp.time_slots:
    #         if slot == selected_slot:
    #             screen.ids[slot].md_bg_color = (0, 1, 0, 1)
    #         else:
    #             screen.ids[slot].md_bg_color = (1, 0, 0, 1)
    #
    # def slot_save(self, instance, value, date_range):
    #     # the date string in "year-month-day" format
    #     date_object = datetime.strptime(str(value), "%Y-%m-%d")
    #     # Format the date as "day-month-year"
    #     formatted_date = date_object.strftime("%d-%m-%Y")
    #     self.screen = Builder.load_file("slot_booking.kv")
    #     screen = self.root.current_screen
    #     book_slot = app_tables.book_slot.search(book_date=formatted_date)
    #     book_times = [row['book_time'] for row in book_slot]
    #     print(formatted_date, book_times)
    #     for slots in LoginApp.time_slots:
    #             screen.ids[slots].disabled = False
    #             if not book_times:
    #                 print(book_times)
    #                 for slots in LoginApp.time_slots:
    #                     screen.ids[slots].disabled = False
    #             elif book_times:
    #                 for slots in book_times:
    #                    screen.ids[slots].disabled = True
    #             else:
    #                 pass
    #     screen.ids.date_choosed.text = formatted_date
    #
    # def slot_cancel(self, instance, value):
    #     print("cancel")
    #     self.screen = Builder.load_file("slot_booking.kv")
    # def slot_date_picker(self):
    #     current_date = datetime.now().date()
    #     date_dialog = MDDatePicker(year=current_date.year, month=current_date.month, day=current_date.day, size_hint=(None, None), size=(150, 150))
    #     date_dialog.bind(on_save=self.slot_save, on_cancel=self.slot_cancel)
    #     date_dialog.open()
    #
    # def pay_now(self, instance, *args):
    #     self.screen = Builder.load_file("slot_booking.kv")
    #     screen = self.root.current_screen
    #     session_date = screen.ids.date_choosed.text
    #     # Extract the username from menu_profile
    #     self.screen = Builder.load_file("client_services.kv")
    #     screen2 = self.root.get_screen('client_services')
    #     username = screen2.ids.username.text
    #     email = screen2.ids.email.text
    #     user = app_tables.users.get(email=email)
    #     id = user['id']
    #     row = app_tables.book_slot.search()
    #     slot_id = len(row)+1
    #     if len(session_date) == 10 and hasattr(self, 'session_time') and self.session_time:
    #         print(username,session_date, self.session_time )
    #         self.root.current = 'payment_page'
    #         current_screen = self.root.current_screen
    #         current_screen.ids.user_name.text = username
    #         current_screen.ids.session_date.text = session_date
    #         current_screen.ids.session_time.text = self.session_time
    #
    #         # app_tables.book_slot.add_row(
    #         #     slot_id=slot_id,
    #         #     user_id=id,
    #         #     username=username,
    #         #     book_date=session_date,
    #         #     book_time=self.session_time
    #         # )
    #         self.root.transition.direction = 'left'
    #         self.root.current = 'payment_page'
    #     elif len(session_date) == 13 and hasattr(self, 'session_time') and self.session_time:
    #         self.show_validation_dialog("Select Date")
    #     elif not hasattr(self, 'session_time') and len(session_date) == 10:
    #         self.show_validation_dialog("Select Time")
    #     else:
    #         self.show_validation_dialog("Select Date and Time")

#-------------------------------Razorpay-flow------------------------------------

    def razor_pay(self, instance):
        client = razorpay.Client(auth=('rzp_test_kOpS7Ythlfb1Ho', 'OzPZyPbsOV0AlADilk4wkgv9'))

        # Create an order
        order_amount = 5000  # Amount in paise (e.g., 50000 paise = 500 INR)
        order_currency = 'INR'
        order_receipt = 'order_rcptid_12'

        order_data = {
            'amount': order_amount,
            'currency': order_currency,
            'receipt': order_receipt,
            'payment_capture': 1  # Automatically capture payment when order is created
        }

        try:
            order = client.order.create(data=order_data)

            # Get the order ID
            order_id = order['id']
            # client.payment.launch(order_id)

            # Construct the payment URL
            payment_url = f"https://rzp_test_kOpS7Ythlfb1Ho.api.razorpay.com/v1/checkout/{order_id}"
            self.open_payment_gateway(payment_url)

        except Exception as e:
            print("An error occurred while creating the order:", str(e))

    def open_payment_gateway(self, payment_url):
        # Replace this with actual code to open the payment gateway URL
        print(f"Opening Razorpay payment gateway: {payment_url}")
        # # Create the Razorpay checkout URL
        # razorpay_key_id = 'rzp_test_kOpS7Ythlfb1Ho'
        # razorpay_checkout_url = f'https://checkout.razorpay.com/v1/checkout.js?key={razorpay_key_id}'
        # webbrowser(razorpay_checkout_url)

        # Open the Razorpay checkout in a WebView
        # webbrowser.create_window('Razorpay Checkout', razorpay_checkout_url, width=800, height=600, resizable=True)
        #
        # # payment_page page logic
        # layout = BoxLayout(orientation='vertical')
        #
        # # Create a WebView to display the Razorpay payment page
        # webview = WebView(url='payment_url', size_hint=(1, 1))
        # layout.add_widget(webview)
        #
        # # Add a back button
        # back_button = Button(text='Back to App', size_hint=(1, 0.1))
        # back_button.bind(on_press=self.back_to_app)
        # layout.add_widget(back_button)
        #
    # def open_payment_gateway(self, payment_url):
    #     # Replace this with actual code to open the payment gateway URL
    #     print(f"Opening Razorpay payment gateway: {payment_url}")
    #
    #     # payment_page page logic
    #     layout = BoxLayout(orientation='vertical')
    #
    #     # Create a WebView to display the Razorpay payment page
    #     webview = WebView(url='payment_url', size_hint=(1, 1))
    #     layout.add_widget(webview)
    #
    #     # Add a back button
    #     back_button = Button(text='Back to App', size_hint=(1, 0.1))
    #     back_button.bind(on_press=self.back_to_app)
    #     layout.add_widget(back_button)

        # return layout

    # def on_pay_button_pressed(self, instance):
    #     client = razorpay.Client(api_key="YOUR_API_KEY", api_secret="YOUR_API_SECRET")
    #
    #     order = client.order.create(amount=10000, currency="INR")
    #
    #     client.payment.launch(order_id=order["id"])
    #
    #     client.payment.on("success", self.on_payment_success)
    #
    # def on_payment_success(self, payment):
    #     self.label.text = "Payment successful!"


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

    app = LoginApp()
    Window.bind(on_request_close=app.stop)
    app.run()