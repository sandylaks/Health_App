import re

from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager
from kivy.core.text import LabelBase
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog

Window.size = (310, 580)


# Create the main app class
class LoginApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.screen = Builder.load_file("signup.kv")

    def set_error_message(self, instance_signup_email):
        # Validation logic
        email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not self.email or not re.match(email_regex, self.email):
            self.screen.ids.signup_email.error = True
        elif not self.password or len(self.password) < 6:
            self.screen.ids.signup_password.error = True
        elif not self.phone or len(self.phone) != 10:
            self.screen.ids.signup_phone.error = True
        elif not self.pincode or len(self.pincode) != 6:
            self.screen.ids.signup_pincode.error = True
        else:
            self.root.manager.transition.direction = "left"
            self.root.manager.current = "login.kv"

    def validate_inputs(self, instance, *args):
        self.email = self.screen.ids.signup_email.bind(
            on_text_validate=self.set_error_message,
            on_focus=self.set_error_message,
        )
        self.password = self.screen.ids.signup_password.bind(
            on_text_validate=self.set_error_message,
            on_focus=self.set_error_message,
        )
        self.phone = self.screen.ids.signup_phone.bind(
            on_text_validate=self.set_error_message,
            on_focus=self.set_error_message,
        )
        self.pincode = self.screen.ids.signup_pincode.bind(
            on_text_validate=self.set_error_message,
            on_focus=self.set_error_message,
        )
        return self.screen


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
        screen_manager.add_widget(Builder.load_file("service_provider.kv"))
        screen_manager.add_widget(Builder.load_file("client_services.kv"))
        return screen_manager


# Run the app
if __name__ == '__main__':
    LoginApp().run()
