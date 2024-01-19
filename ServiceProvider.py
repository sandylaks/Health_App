import kivy
import re
from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.pickers import MDDatePicker
from kivy.properties import ObjectProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.animation import Animation
from kivy.metrics import dp
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.button import Button
#from plyer import filechooser
from kivymd.uix.filemanager import MDFileManager
import sqlite3
import os
import base64
from kivy.uix.image import AsyncImage
from kivy.uix.image import Image

from kivymd.app import MDApp
from kivy.clock import Clock
from kivymd.uix.behaviors import CommonElevationBehavior


Builder.load_file("service_register_form.kv")
Builder.load_file("service_provider.kv")
Builder.load_file("service_provider_main_page.kv")
Builder.load_file("ambulance_register_form.kv")
Builder.load_file("gym_register_form.kv")

#----------------------Rigistration form--------------------
class BaseRegistrationScreen(MDScreen):


    #------------------dropdowns---------------
    menu = ObjectProperty(None)
    menu2 = ObjectProperty(None)
    def open_dropdown(self, widget):
        if not self.menu:
            # Dropdown items
            cities = ["India", "America", "Russia", "China"]
            items = [
                {
                    "text": city,
                    "viewclass": "OneLineListItem",
                    "on_release": lambda x=city: self.select_city(x),
                } for city in cities
            ]
            # Create the dropdown menu with the caller property set
            self.menu = MDDropdownMenu(
                caller=widget,
                items=items,
                width_mult=3,
                max_height=300,
            )
        else:
            self.menu.dismiss()  # Dismiss if already open

        # Open the dropdown menu
        self.menu.open()

    def select_city(self, selected_city):
        # Callback function when a city is selected
        self.ids.dropdown_nation.text = selected_city  # Update the text field
        self.menu.dismiss()
    def open_dropdown2(self,widget):

        if not self.menu2:
            # Dropdown items
            cities = [
                        "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh",
                        "Goa", "Gujarat", "Haryana", "Himachal Pradesh", "Jharkhand",
                        "Karnataka", "Kerala", "Madhya Pradesh", "Maharashtra", "Manipur",
                        "Meghalaya", "Mizoram", "Nagaland", "Odisha", "Punjab", "Rajasthan",
                        "Sikkim", "Tamil Nadu", "Telangana", "Tripura", "Uttar Pradesh",
                        "Uttarakhand", "West Bengal", "Andaman and Nicobar Islands",
                        "Chandigarh", "Dadra and Nagar Haveli and Daman and Diu",
                        "Lakshadweep", "Delhi", "Puducherry"
                    ]
            items = [
                {
                    "text": city,
                    "viewclass": "OneLineListItem",
                    "on_release": lambda x=city: self.select_state(x),
                } for city in cities
            ]
            # Create the dropdown menu
            self.menu2 = MDDropdownMenu(
                items=items,
                width_mult=6,
                max_height=400,
                pos_hint={'center_x':.1,'center_y':.9}
            )
        else:
            self.menu2.dismiss()  # Dismiss if already open

        # Set the caller and open the dropdown menu
        self.menu2.caller = self.ids.dropdown_state
        self.menu2.open()

    def select_state(self, select_state):
        # Callback function when a city is selected
        #print(select_state)
        self.ids.dropdown_state.text = select_state  # Update the text field
        self.menu2.dismiss()  # Dismiss the menu


    def on_save(self, instance, value, date_range):
        self.ids.extra_info2.text = str(value)

    # click Cancel
    def on_cancel(self, instance, value):
        #print("cancel")
        instance.dismiss()

    def show_date_picker(self,arg):
        date_dialog = MDDatePicker( size_hint=(None, None), size=(150, 150))
        date_dialog.bind(on_save=self.on_save, on_cancel=self.on_cancel)
        date_dialog.open()
        self.ids.extra_info2.text=''
#------------------------------upload--docs--------------------------
    # def open_file_chooser(self):
    #     file_chooser = FileChooserListView(filters=["*.pdf", "*.doc", "*.docx", "*.png", "*.jpg"])
    #     file_chooser.bind(on_selection=self.file_selected)
    #
    #     popup = Popup(title="Choose a file", content=file_chooser, size_hint=(0.9, 0.9))
    #     popup.open()
    #
    #     self.file_chooser_popup = popup
    #
    # def file_selected(self, instance, selected_files):
    #     # Check if any files are selected
    #     if selected_files:
    #         selected_file = selected_files[0]  # first selected file
    #         # Do something with the selected file path, like uploading it to the database
    #         with open(selected_file, 'rb') as file:
    #             file_content = file.read()
    #         print(f"Selected file: {selected_file}")
    #         selected_file_label = self.ids.selected_file_label
    #         selected_file_label.text = f"{selected_file}"
    #
    #     self.file_chooser_popup.dismiss()

    def show_tooltip(self, text, tooltip_text):
        tooltip = MDTooltip(text=tooltip_text)
        tooltip.ids.container.add_widget(MDLabel(text=text))
        tooltip.show()

    def file_manager_open(self):
        self.connection = sqlite3.connect('users.db')  # Replace with your database name
        self.cursor = self.connection.cursor()
        self.cursor.execute('''
                   CREATE TABLE IF NOT EXISTS documents (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       file_name TEXT,
                       file_data BLOB
                   )
               ''')
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager,
            select_path=self.select_path,

        )
        self.file_manager.show('/')  # Initial directory when the file manager is opened

    def select_path(self, path):
        if self.ids == "file_selected_1":
            self.ids.file_selected_1.text = path
            self.file_manager.close()
        else:
            self.ids.file_selected_2.text = path
            self.file_manager.close()

    def upload_file(self):
        if self.ids == "file_selected_1":
            file_path = self.ids.file_selected_1.text
        else:
            file_path = self.ids.file_selected_2.text
        if file_path:
            file_name = os.path.basename(file_path)
            file_data = self.read_file(file_path)
            self.save_to_database(file_name, file_data)
            if self.ids == "file_selected_1":
                self.ids.file_selected_1.text = f'{file_name} uploded'
            else:
                self.ids.file_selected_2.text = f'{file_name} uploded'

        # if file_path and os.path.isfile(file_path):
        #     self.ids.file_display.source = file_path

    def read_file(self, file_path):
        with open(file_path, 'rb') as file:
            return file.read()

    def save_to_database(self, file_name, file_data):
        self.cursor.execute('INSERT INTO documents (file_name, file_data) VALUES (?, ?)', (file_name, file_data))
        self.connection.commit()

    # def display_file(self, file_path):
    #     file_display = self.ids.file_display
    #
    #     if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
    #         # Display image
    #         image = AsyncImage(source=file_path, allow_stretch=True)
    #         file_display.clear_widgets()
    #         file_display.add_widget(image)
    #     elif file_path.lower().endswith('.pdf'):
    #         # Display PDF (requires additional dependencies)
    #         label = Label(text="PDF files are not supported in this example.")
    #         file_display.clear_widgets()
    #         file_display.add_widget(label)
    #     else:
    #         # Unsupported file type
    #         label = Label(text="Unsupported file type.")
    #         file_display.clear_widgets()
    #         file_display.add_widget(label)

    def exit_manager(self, *args):
        self.file_manager.close()


#----------------------------------registration validation-------------
    def registration_submit_button(self, instance):
        service_provider_name = self.ids.service_provider_name.text
        service_provider_email = self.ids.service_provider_email.text
        service_provider_password = self.ids.service_provider_password.text
        service_provider_phoneno = self.ids.service_provider_phoneno.text
        service_provider_address = self.ids.service_provider_address.text
        dropdown_nation=self.ids.dropdown_nation.text
        dropdown_state=self.ids.dropdown_state.text
        service_provider_pincode=self.ids.service_provider_pincode.text
        extra_info=self.ids.extra_info.text
        extra_info2=self.ids.extra_info2.text
        # print(service_provider_name)
        # print(service_provider_email)
        # print(service_provider_password)
        # print(service_provider_address)
        # print(service_provider_phoneno)
        # print(dropdown_nation)
        # print(dropdown_state)
        # print(service_provider_pincode)
        # print(extra_info)
        # print(extra_info2)

        # Validation logic
        email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        is_valid_password, password_error_message = self.validate_password(service_provider_password)

        if not service_provider_name:
            self.ids.service_provider_name.error = True
            self.ids.service_provider_name.helper_text = "This field is required."
            self.ids.service_provider_name.required = True
        elif not service_provider_email or not re.match(email_regex, service_provider_email):
            self.ids.service_provider_email.error = True
            self.ids.service_provider_email.helper_text = "Invalid email format."
            self.ids.service_provider_email.required = True
        elif not is_valid_password:
            self.ids.service_provider_password.error = True
            self.ids.service_provider_password.helper_text =  password_error_message
            self.ids.service_provider_password.required = True
        elif not service_provider_phoneno or len(service_provider_phoneno) != 10:
            self.ids.service_provider_phoneno.error = True
            self.ids.service_provider_phoneno.helper_text = "Invalid phone number (10 digits required)."
            self.ids.service_provider_phoneno.required = True
        elif not service_provider_address:
            self.ids.service_provider_address.error = True
            self.ids.service_provider_address.helper_text = "This field is required."
            self.ids.service_provider_address.required = True
        elif not dropdown_nation:
            self.ids.dropdown_nation.error = True
            self.ids.dropdown_nation.helper_text = "Please select a nation."
            # self.ids.dropdown_nation.required = True
        elif not dropdown_state:
            self.ids.dropdown_state.error = True
            self.ids.dropdown_state.helper_text = "Please select a state."
            # self.ids.dropdown_state.required = True
        elif not service_provider_pincode or len(service_provider_pincode) != 6:
            self.ids.service_provider_pincode.error = True
            self.ids.service_provider_pincode.helper_text = "Invalid pincode (6 digits required)."
            self.ids.service_provider_pincode.required = True
        elif not extra_info:
            self.ids.extra_info.error = True
            self.ids.extra_info.helper_text = "This field is required."
            self.ids.extra_info.required = True
        elif not extra_info2:
            self.ids.extra_info2.error = True
            self.ids.extra_info2.helper_text = "This field is required."
            # self.ids.est_year.required = True

        else:
            # All validations passed; proceed with registration process
            #If validation is successful, insert into the database
            # cursor.execute('''
            #             INSERT INTO users (username, email, password, phone, pincode)
            #             VALUES (?, ?, ?, ?, ?)
            #         ''', (username, email, password, phone, pincode))
            # conn.commit()
            # Navigate to the success screen
            app = MDApp.get_running_app()
            app.root.transition.direction = "left"
            app.root.current = "login"

    # password validation
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


class ServiceRegister(BaseRegistrationScreen):
    # Additional functionalities specific to ServiceRegister
    pass

class ServiceRegisterGym(BaseRegistrationScreen):
    # Additional functionalities specific to ServiceRegisterGym
    pass

class ServiceRegisterAmbulance(BaseRegistrationScreen):
    # Additional functionalities specific to ServiceRegisterAmbulance
    pass

#------------------------ServiceProvider--------------------

class ServiceProvider(MDScreen):

    def animate_button(self, button_id):
        original_button_size = (dp(290), dp(150))
        original_image_size = (dp(290), dp(150))

        # Create animation for the button size
        anim_button = Animation(size=(dp(280), dp(140)),  duration=0.2, transition="linear")
        anim_button += Animation(size=original_button_size,duration=0.2)

        # Create animation for the image size
        anim_image = Animation( size=(dp(280), dp(140)),duration=0.2, transition="linear")
        anim_image += Animation(size=original_image_size, duration=0.2)

        anim_button.start(self.ids[button_id])
        anim_image.start(self.ids[button_id].children[0])

        self.ids[button_id].elevation_normal = 0

        Clock.schedule_once(lambda dt: self.transition_to_service_register_form(button_id), 0.5)

    def transition_to_service_register_form(self, button_id):
        app = MDApp.get_running_app()
        app.root.transition.direction = "left"

        if button_id == 'hospital_button':
            app.root.current = "service_register_form"
        elif button_id == 'ambulance_button':
            app.root.current = "ambulance_register_form"
        elif button_id == 'gym_button':
            app.root.current = "gym_register_form"
        # Add more conditions as needed for other buttons

#-------------------service provider main-----------------------
class ServiceProviderMain(MDScreen):
    menu = ObjectProperty(None)
    def service_button(self,button):
        if not self.menu:
            cities = ["Settings", "Notification"]
            items = [
                {
                    "text": city,
                    "viewclass": "OneLineListItem",
                    "on_release": lambda x=city: self.select_city(x),
                } for city in cities
            ]

            # Use the first button from right_action_items as the caller



            self.menu = MDDropdownMenu(
                caller=button,
                items=items,
                width_mult=3,
                elevation=2,

                max_height = dp(100),

            )
        else:
            self.menu.dismiss()

        self.menu.open()

    def select_city(self, option):
        # Callback function when a city is selected
        if option == 'Settings':
            self.settings()
        elif option == 'Notification':
            self.notification_button_action()

        self.menu.dismiss()

    def settings(self):
        print("Settings")

    def notification_button_action(self):
        print("Notification")


    def sign_out_button_action(self):
        app = MDApp.get_running_app()
        app.root.transition.direction = "left"
        app.root.current = "login"
class ServiceProfile(MDScreen):
    pass

class ServiceNotification(MDScreen):
    pass
class ServiceSlotAdding(BaseRegistrationScreen):
    pass
class ServiceSupport(MDScreen):
    pass