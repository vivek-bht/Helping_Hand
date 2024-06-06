from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.core.window import Window
import subprocess

class Instructions(App):
    def build(self):
        Window.bind(on_request_close=Window.close)
        Window.size = (1366, 718)
        Window.top = 30
        Window.left = 0

        layout = BoxLayout(orientation='vertical')
        self.welcome_label = Label(
            text="Welcome to Helping Hand\n\n"
                 "We will be your hand and help you navigate your computer just using your face! Soon, a window will appear with your face and a circle around your nose. \n"
                 "Keep your nose inside the circle to stop the cursor else it will follow the angle your nose makes with the circle's center.",
            font_size='20sp',
            halign='center'
        )

        self.countdown_label = Label(
            text="10",
            font_size='50sp',
            bold=True,
            halign='center'
        )
        layout.add_widget(self.welcome_label)
        layout.add_widget(self.countdown_label)

        self.seconds_left = 10
        Clock.schedule_interval(self.update_countdown, 1)
        return layout

    def update_countdown(self, dt):
        self.seconds_left -= 1
        self.countdown_label.text = str(self.seconds_left)
        
        if self.seconds_left <= 0:
            Clock.unschedule(self.update_countdown)
            Window.close()

if __name__ == '__main__':
    Instructions().run()
    subprocess.run(['python', 'multi.py'])
