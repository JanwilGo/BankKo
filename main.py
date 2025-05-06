from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup

class LoginScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', padding=20, spacing=15, **kwargs)

        # Header
        header = BoxLayout(size_hint_y=None, height=80)
        header.add_widget(Label(text="Welcome to BankKo", font_size=24, bold=True, color=[1,1,1,1]))
        self.add_widget(header)

        # Email
        self.add_widget(Label(text="Username (Email):", font_size=16))
        self.email_input = TextInput(multiline=False, font_size=16)
        self.add_widget(self.email_input)

        # Password
        self.add_widget(Label(text="Password:", font_size=16))
        self.password_input = TextInput(password=True, multiline=False, font_size=16)
        self.add_widget(self.password_input)

        # Buttons
        btns = BoxLayout(spacing=10, size_hint_y=None, height=50)

        login_btn = Button(text="Login", background_color=[0.18, 0.50, 0.93, 1], bold=True)
        login_btn.bind(on_press=self.login)
        btns.add_widget(login_btn)

        signup_btn = Button(text="Sign Up", background_color=[0.30, 0.69, 0.31, 1], bold=True)
        signup_btn.bind(on_press=self.signup)
        btns.add_widget(signup_btn)

        self.add_widget(btns)

    def login(self, instance):
        email = self.email_input.text
        password = self.password_input.text
        if email == "test@example.com" and password == "1234":
            self.show_popup("Login Success", "Welcome to BanKo!")
        else:
            self.show_popup("Login Failed", "Invalid login details.")

    def signup(self, instance):
        self.show_popup("Sign Up", "Redirecting to signup...")

    def show_popup(self, title, message):
        popup = Popup(title=title, content=Label(text=message),
                      size_hint=(None, None), size=(300, 200))
        popup.open()

class BankKoApp(App):
    def build(self):
        return LoginScreen()

if __name__ == '__main__':
    BankKoApp().run()
