from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.core.window import Window
import subprocess
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.graphics import Color, Ellipse
class Paraconnect(App):
    def build(self):
        Window.set_icon('logo2.png')
        Window.bind(on_request_close=Window.close)
        Window.size = (1366, 692)
        Window.top = 30
        Window.left = 0
        Window.always_on_top = True
        layout =FloatLayout()
        background = Image(source='pikaso_texttoimage_35mm-film-photography-Highly-detailed-stick-figure.jpeg', allow_stretch=True, keep_ratio=False, opacity = 0.5 )
        layout.add_widget(background)
        heading = Label(text="ParaConnect",
                        font_name = "Lobster-Regular.ttf",
                        font_size=80,
                        color=(0.65, 0.65, 0.65, 0.5),  
                        size_hint=(None, None),
                        pos_hint={'center_x': 0.505, 'top': 0.995}
                        )
        layout.add_widget(heading)

        subheading = Label(text="Express to Connect, Smile to Navigate",
                           font_size=20,
                           color=(.65, .65, .65, .5), 
                           size_hint=(None, None),
                           pos_hint={'center_x': 0.505, 'top': 0.905})
        layout.add_widget(subheading)
        self.countdown_label = Label(
            text="10",
            font_size='50sp',
            bold=True,
            halign='center'
        )
        layout.add_widget(self.countdown_label)
       
        self.label = Label(text="[size=32]Instructions:-[/size] \n"
                           "\n1.We will be your hand and help you navigate your computer just using your face! \n Soon, a window will appear with your face and a circle around your nose. \n"
                           "\n2.Keep your nose inside the circle to stop the cursor else it will follow the angle your nose makes with the circle's center.\n"
                           "\n3.for left clicking blink your left eye\n"
                           "\n4.For right clicking blink your right eye.\n"
                           "\n5.for double clicking close your left eye for 2 seconds.\n"
                           "\nFor activating the onscreen keyboard left click on keyboard toggle button: ",
                           markup=True ,font_size='22sp',size_hint=(None, None), size=(300, 50), pos_hint={'x': 0.4, 'y': 0.2}, font_name = "Roboto", color = (.65,.65,.65,1), bold = True)
        layout.add_widget(self.label)

        Clock.schedule_once(self.change_text, 10)
        
        self.seconds_left = 40
        self.multi_process_started = False
        Clock.schedule_interval(self.update_countdown, 1)
        return layout
    
    def change_text(self, dt):
        self.label.text ="[size=32]Onscreen Keyboard:-[/size]\n""\n1. When you gaze on the sector of the circle containing the keys it will turn blue,\n    and the key that you are gazing at will turn darker blue.\n""\n2. If you want to type the key you're looking at (the one tha turns darker shade of blue) blink at it.\n""\n3. If you want to close the keyboard blink once while gazing at the KMO button\n""\n4. Blink on others key for activating the voice mode take the cursor to the toggle voice mode and blink left eye"
        # self.label.padding = (20,20)
        self.label.pos_hint = {'x': 0.4, 'y': 0.18}
        self.markup = True
        Clock.schedule_once(self.change_text2,10)
        
    def change_text2(self, dt):
        self.label.text ="[size=32]Offline Commands:-[/size]\n""\n1. Double click: performs a double click\n""\n2. Single click: performs a single click.\n""\n3. Right click : performs a right click.\n""\n4. Scroll up: scrolls up the screen\n""\n5. Scroll down: scrolls down the screen\n""\n5. Scroll mode on : activates the scroll mode \n""\n6.scroll mode off: deactivates the scroll mode.\n""\n7. Typing mode on: turns on the typing mode\n""\n8.typing mode off: turns off the typing mode\n""\n8. Delete:deletes the last entered word"
        self.label.pos_hint = {'x': 0.1, 'y': 0.3}
        # self.label.padding = (20,20)
        Clock.schedule_once(self.change_text3,10)
    
    def change_text4(self, dt):
        self.label.text = ""
        
    def change_text3(self, dt):
        self.label.text ="[size=32]Online commands:[/size]\n""\n1.All the commands that were given in offline mode\n" "\n2. Query + wikipedia: gives you result for your query available in wikipedia\n" "\n3. Search + query: searches the query in the web browser\n" "\n4. Open google: opens google.com\n""\n5. Open youtube: opens youtube.com\n""\n6.camera: opens the camera \n" "\n7. Take a photo: takes the photo\n""\n8.restart : restarts the computer in 1 minute\n""\n9. Hibernate: puts the computer in sleep\n""\n10. Log off: shuts down the computer"   
        self.label.pos_hint = {'x':0.2, 'y':0.3}
    
    def update_countdown(self, dt):
        self.seconds_left -= 1
        self.countdown_label.text = str(self.seconds_left)
        
        if self.seconds_left <= 0:
            Clock.unschedule(self.update_countdown)
            Window.close()
        
        if self.seconds_left <= 38 and not self.multi_process_started:
            subprocess.Popen(['python', 'multi.py'])
            self.multi_process_started = True

if __name__ == '__main__':
    Paraconnect().run()
