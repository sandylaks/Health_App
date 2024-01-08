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


Builder.load_file("service_register_form.kv")
Builder.load_file("service_provider.kv")
class ServiceRegister(MDScreen):
    menu = ObjectProperty(None)
    menu2 = ObjectProperty(None)


    def open_dropdown(self,widget):

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
            # Create the dropdown menu
            self.menu = MDDropdownMenu(
                items=items,
                width_mult=3,
                max_height=300,
            )
        else:
            self.menu.dismiss()  # Dismiss if already open

        # Set the caller and open the dropdown menu
        self.menu.caller = widget
        self.menu.open()

    def select_city(self, selected_city):
        # print(selected_city)
        # Callback function when a city is selected
        self.ids.dropdown_nation.text = selected_city  # Update the text field
        self.menu.dismiss()  # Dismiss the menu
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
                width_mult=3,
                max_height=300,
            )
        else:
            self.menu2.dismiss()  # Dismiss if already open

        # Set the caller and open the dropdown menu
        self.menu2.caller = widget
        self.menu2.open()

    def select_state(self, select_state):
        # Callback function when a city is selected
        #print(select_state)
        self.ids.dropdown_state.text = select_state  # Update the text field
        self.menu2.dismiss()  # Dismiss the menu


    def on_save(self, instance, value, date_range):
        self.ids.est_year.text = str(value)

    # click Cancel
    def on_cancel(self, instance, value):
        #print("cancel")
        instance.dismiss()

    def show_date_picker(self,arg):
        date_dialog = MDDatePicker( size_hint=(None, None), size=(150, 150))
        date_dialog.bind(on_save=self.on_save, on_cancel=self.on_cancel)
        date_dialog.open()
        self.ids.est_year.text=''

    def registration_submit(self, instance):
        service_provider_name = self.ids.service_provider_name.text
        service_provider_email = self.ids.service_provider_email.text
        service_provider_password = self.ids.service_provider_password.text
        service_provider_phoneno = self.ids.service_provider_phoneno.text
        service_provider_address = self.ids.service_provider_address.text
        dropdown_nation=self.ids.dropdown_nation.text
        dropdown_state=self.ids.dropdown_state.text
        service_provider_pincode=self.ids.service_provider_pincode.text
        hospital_name=self.ids.hospital_name.text
        est_year=self.ids.est_year.text
        print(service_provider_name)
        print(service_provider_email)
        print(service_provider_password)
        print(service_provider_address)
        print(service_provider_phoneno)
        print(dropdown_nation)
        print(dropdown_state)
        print(service_provider_pincode)
        print(hospital_name)
        print(est_year)

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
        elif not hospital_name:
            self.ids.hospital_name.error = True
            self.ids.hospital_name.helper_text = "This field is required."
            self.ids.hospital_name.required = True
        elif not est_year:
            self.ids.est_year.error = True
            self.ids.est_year.helper_text = "This field is required."
            # self.ids.est_year.required = True

        else:
            # All validations passed; proceed with registration process
            pass

    #If validation is successful, insert into the database
            # cursor.execute('''
            #             INSERT INTO users (username, email, password, phone, pincode)
            #             VALUES (?, ?, ?, ?, ?)
            #         ''', (username, email, password, phone, pincode))
            # conn.commit()
            # Navigate to the success screen
            # self.root.transition = SlideTransition(direction='left')
            # self.root.current = 'login'
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
class ServiceProvider(MDScreen):
    pass
    # def on_button_click(self):
    #     # Switch to 'service_register_form' screen
    #     self.manager.transition = SlideTransition(direction='left')
    #     self.manager.current = 'service_register_form'
    #
    #

class ImageButton(ButtonBehavior, Image):
    def zoom_in_image(self):
        self.size_hint = (None, None)
        self.size = (self.width * 1.2, self.height * 1.2)

    def zoom_out_image(self):
        self.size_hint = (None, None)
        self.size = (self.width / 1.2, self.height / 1.2)

    def on_enter(self):
        self.zoom_in_image()

    def on_leave(self):
        self.zoom_out_image()

    # def on_release(self):
    #     # Emit an event to indicate that the button was clicked
    #     self.dispatch('on_button_click')
    #
    # def on_button_click(self):
    #     pass  # This method will be overridden in the parent class


class HoverButton(ButtonBehavior, Image):
    def __init__(self, **kwargs):
        super(HoverButton, self).__init__(**kwargs)
        self.hovered = False

    def on_enter(self):
        self.hovered = True
        self.animate_image()

    def on_leave(self):
        self.hovered = False
        self.animate_image()

    def animate_image(self):
        if self.hovered:
            self.size_hint = (None, None)
            self.size = (self.width * 1.2, self.height * 1.2)
        else:
            self.size_hint = (None, None)
            self.size = (self.width / 1.2, self.height / 1.2)