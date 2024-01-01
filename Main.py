from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager
from kivy.core.text import LabelBase
Window.size = (310, 580)

# Create the main app class
class LoginApp(MDApp):
    def build(self):
        screen_manager = ScreenManager()
        screen_manager.add_widget(Builder.load_file("login.kv"))
        screen_manager.add_widget(Builder.load_file("main_sc.kv"))
        screen_manager.add_widget(Builder.load_file("signup.kv"))
        return screen_manager


# Run the app
if __name__ == '__main__':
    LoginApp().run()
