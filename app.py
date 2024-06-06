from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.graphics.texture import Texture
from kivy.graphics import Color, Line, Ellipse
from kivy.clock import Clock
from kivy.core.window import Window
import pyautogui
import cv2
import mediapipe as mp
import numpy as np
from math import cos, sin, pi
from kivy.uix.floatlayout import FloatLayout

class NextApp(App):
    def __init__(self, shared_dict, lock, **kwargs):
        super(NextApp, self).__init__(**kwargs)
        self.shared_dict = shared_dict
        self.lock = lock
        self.face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True, max_num_faces=1)
        self.center_x = 300
        self.center_y = 250
        self.keys = [
            ['W', 'Y', 'S', 'B', 'H', 'V', 'K', 'F'],
            ['G', 'N', 'I', 'E', 'T', 'D', 'L', 'C'],
            ['P', 'O', 'A', 'M', 'U', 'Q', 'J', 'KMO'],
            ['Z', 'Other', '*', 'X', 'Options', 'R', 'Space', 'Enter']
        ]
        self.radius = min(Window.width, Window.height) / 2

    def build(self):
        self.root = FloatLayout()
        self.setup_layout()
        Window.always_on_top = True
        Clock.schedule_interval(self.check_position, 0.1)
        Clock.schedule_interval(self.comp_update, 1.0 / 30.0)
        return self.root

    def setup_layout(self):
        self.root.clear_widgets()
        if not self.shared_dict['keyboard_mode']:
            self.new_layout = BoxLayout(orientation='vertical')
            self.message_label = Label(
                text=self.shared_dict['msg'],
                size_hint=(1, None),
                height=50,
                color=(0, 1, 1, 1)
            )
            self.new_layout.add_widget(self.message_label)
            self.img = Image()
            self.new_layout.add_widget(self.img)

            self.button_layout = BoxLayout(size_hint=(1, None), height=50)
            self.toggle_keyboard_btn = Button(text='Toggle Keyboard Mode', on_press=self.toggle_keyboard_mode)
            self.toggle_voice_btn = Button(text='Toggle Voice Mode',  on_press=self.toggle_keyboard_mode)
            self.button_layout.add_widget(self.toggle_keyboard_btn)
            self.button_layout.add_widget(self.toggle_voice_btn)
            self.new_layout.add_widget(self.button_layout)
            with self.new_layout.canvas:
                Color(0, 0, 1, 1)
                self.circle = Line(circle=(self.center_x, self.center_y, 50), width=1)
            Clock.schedule_interval(self.comp_update, 1.0 / 30.0)
            self.root.add_widget(self.new_layout)
        else:
            self.layout = FloatLayout()
            self.center_x = Window.width / 2
            self.center_y = Window.height / 2
            self.radius = min(Window.width, Window.height) / 2
            Window.bind(on_resize=self.on_window_resize)
            Clock.schedule_interval(self.update_canvas, 0.1)
            self.root.add_widget(self.layout)

    def toggle_keyboard_mode(self, instance):
        self.shared_dict['keyboard_mode'] = not self.shared_dict['keyboard_mode']
        self.setup_layout()
    def toggle_keyboard_mode(self, instance):
        self.shared_dict['voice_mode'] = True

    def on_window_resize(self, window, width, height):
        self.center_x = width / 2
        self.center_y = height / 2
        self.radius = min(width, height) / 2
        self.update_canvas()

    def update_canvas(self, dt=None):
        self.layout.canvas.clear()
        self.layout.clear_widgets()
        self.draw_keyboard()
        self.draw_key_labels()
        self.on_touch_down()

    def draw_keyboard(self):
        angle = (self.shared_dict['angle'] + 2 * np.pi) % (2 * np.pi)
        segment = int(angle // (pi / 4))
        r = self.shared_dict['distance']
        ring = int(r // (self.radius / 4))

        with self.layout.canvas:
            Color(0, 0.5, 1)
            Ellipse(pos=(self.center_x - self.radius, self.center_y - self.radius), size=(2 * self.radius, 2 * self.radius))
            segment_angle = pi / 4

            for i in range(8):
                for j in range(4):
                    if self.keys[j][i]:
                        mid_angle = (i * segment_angle) + (segment_angle / 2)
                        inner_radius = (j + 1) * (self.radius / 4)
                        inner_to_inner_radius = j * (self.radius / 4)
                        label_radius = ((j + 1) * (self.radius / 4)) - (self.radius / 8)
                        label_x = self.center_x + label_radius * cos(mid_angle)
                        label_y = self.center_y + label_radius * sin(mid_angle)

                        if self.keys[j][i] == self.keys[ring][segment]:
                            Color(0, 0, 1)
                            angle_start_deg = (i + 2) * segment_angle * (180 / pi)
                            angle_end_deg = ((i + 2) * segment_angle + segment_angle) * (180 / pi)
                            Ellipse(pos=(self.center_x - self.radius, self.center_y - self.radius), size=(self.radius * 2, self.radius * 2), angle_start=angle_start_deg, angle_end=angle_end_deg)
                            Color(0, 0, 0.5)
                            angle_start_deg = (i + 2) * segment_angle * (180 / pi)
                            angle_end_deg = ((i + 2) * segment_angle + segment_angle) * (180 / pi)
                            Ellipse(pos=(self.center_x - inner_radius, self.center_y - inner_radius), size=(inner_radius * 2, inner_radius * 2), angle_start=angle_start_deg, angle_end=angle_end_deg)
                            Color(0, 0, 1)
                            angle_start_deg = (i + 2) * segment_angle * (180 / pi)
                            angle_end_deg = ((i + 2) * segment_angle + segment_angle) * (180 / pi)
                            Ellipse(pos=(self.center_x - inner_to_inner_radius, self.center_y - inner_to_inner_radius), size=(inner_to_inner_radius * 2, inner_to_inner_radius * 2), angle_start=angle_start_deg, angle_end=angle_end_deg)

                        key_label = Label(
                            text=self.keys[j][i],
                            pos=(label_x - 20, label_y - 20),
                            size_hint=(None, None),
                            size=(40, 40),
                            color=(1, 1, 1, 1)
                        )
                        self.layout.add_widget(key_label)

            Color(0, 0, 0)
            self.draw_guidelines(segment_angle)

    def draw_guidelines(self, segment_angle):
        for i in range(8):
            start_angle = i * segment_angle
            Line(
                points=[
                    self.center_x, self.center_y,
                    self.center_x + self.radius * cos(start_angle),
                    self.center_y + self.radius * sin(start_angle)
                ], width=2
            )
        for j in range(1, 5):
            Line(circle=(self.center_x, self.center_y, j * (self.radius / 4)), width=2)

    def draw_key_labels(self):
      segment_angle = pi / 4

      for i in range(8):
          for j in range(4):
              if self.keys[j][i]:
                  mid_angle = (i * segment_angle) + (segment_angle / 2)
                  label_radius = ((j + 1) * (self.radius / 4)) - (self.radius / 8)
                  label_x = self.center_x + label_radius * cos(mid_angle)
                  label_y = self.center_y + label_radius * sin(mid_angle)
                  key_label = Label(
                      text=self.keys[j][i],
                      pos=(label_x - 20, label_y - 20),
                      size_hint=(None, None),
                      size=(40, 40),
                      color=(1, 1, 1, 1)
                  )
                  self.layout.add_widget(key_label)        

    def on_touch_down(self):
        self.radius = min(Window.width, Window.height) / 2
        angle = (self.shared_dict['angle'] + 2 * np.pi) % (2 * np.pi)
        segment = int(angle // (pi / 4))
        r = self.shared_dict['distance']
        ring = int(r // (self.radius / 4))
        keys = self.keys

        if ring < 4:
            key = keys[ring][segment]
            if key:
                if key == 'KMO':
                    self.shared_dict['keyboard_mode'] = False
                    self.setup_layout()
                print(f"Key pressed: {key}")
                self.shared_dict['blink'] = False
                self.shared_dict['key'] = key

    def check_position(self, dt):
        x, y = pyautogui.position()
        if 736 <= x <= 766 and 30 <= y <= 480:
            Window.size = (600, 500)
            Window.top = 30
            Window.left = 0
        else:
            Window.size = (600, 500)
            Window.top = 30
            Window.left = 766

    def comp_update(self, dt):
        ret, frame = self.capture.read()
        if ret:
            frame = cv2.flip(frame, 1)
            if self.lock:
                with self.lock:
                    self.shared_dict['image'].append(frame)

            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.face_mesh.process(rgb_frame)
            frame_h, frame_w, _ = frame.shape

            if results.multi_face_landmarks:
                landmarks = results.multi_face_landmarks[0].landmark
                nose_tip = landmarks[1]
                x = int(nose_tip.x * frame_w)
                y = int(nose_tip.y * frame_h)
                self.shared_dict['distance'] = np.sqrt((x - 320) ** 2 + (y - 240) ** 2)
                self.shared_dict['angle'] = np.arctan2(y - 240, x - 320)

                cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)
                cv2.line(frame, (320, 240), (x, y), (0, 255, 0), 2)
                if not self.shared_dict['keyboard_mode'] and self.shared_dict['distance'] > 50:
                    dx = int(15 * np.cos(self.shared_dict['angle']))
                    dy = int(15 * np.sin(self.shared_dict['angle']))
                    pyautogui.moveRel(dx, dy, duration=0.1)
            buf = cv2.flip(frame, 0).tostring()
            texture = Texture.create(size=(frame_w, frame_h), colorfmt='bgr')
            texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            self.img.texture = texture

    def on_start(self):
        self.capture = cv2.VideoCapture(0)

    def on_stop(self):
        self.capture.release()


if __name__ == '__main__':
    pass