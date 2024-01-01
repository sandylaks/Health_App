from kivy.lang import Builder
from kivymd.app import MDApp


# Define the KV language string
kv_string = '''
BoxLayout:
    orientation: 'vertical'

    MDTopAppBar:
        title: 'Login Page'
        md_bg_color: app.theme_cls.primary_color
        specific_text_color: 1, 1, 1, 1

    MDScreen:

        MDBoxLayout:
            orientation: 'vertical'
            spacing: '10dp'
            padding: '10dp'
            size_hint_y: None
            height: self.minimum_height

            MDLabel:
                text: 'Login'
                font_style: 'H4'
                theme_text_color: 'Secondary'
                halign: 'center'

            MDTextField:
                id: username_field
                hint_text: 'Username'
                icon_right: 'account'
                color_active: app.theme_cls.primary_color
                size_hint_y: None
                height: '40dp'
                radius: [10, 10, 10, 10]

            MDTextField:
                id: password_field
                hint_text: 'Password'
                password: True
                icon_right: 'key-variant'
                color_active: app.theme_cls.primary_color
                size_hint_y: None
                height: '40dp'
                radius: [10, 10, 10, 10]

            MDRaisedButton:
                text: 'Login'
                on_release: app.login()
                pos_hint: {'center_x': 0.5}
                elevation_normal: 8
                md_bg_color: app.theme_cls.primary_color

            MDLabel:
                text: "Don\'t have an account? Sign Up"
                halign: 'center'
                theme_text_color: 'Hint'

            MDRaisedButton:
                text: 'Sign Up'
                on_release: app.sign_up()
                pos_hint: {'center_x': 0.5}
                elevation_normal: 8
                md_bg_color: app.theme_cls.primary_color
'''

# Create the main app class
class LoginApp(MDApp):
    def build(self):
        return Builder.load_string(kv_string)

    def login(self):
        username = self.root.ids.username_field.text
        password = self.root.ids.password_field.text

        # Add your login logic here
        print(f'Login with username: {username}, password: {password}')

    def sign_up(self):
        # Add your sign-up logic here
        print('Redirect to sign-up page')

# Run the app
if __name__ == '__main__':
    LoginApp().run()
