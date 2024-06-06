import cv2
import dlib
import numpy as np
from imutils import face_utils
from keras.models import load_model
import pyautogui
import time
import threading

B_SIZE = (34, 26)
frames_to_blink = 4
blinking_frames = 0
left_wink_start_time = None
right_wink_start_time = None
scroll_mode = False
DOUBLE_CLICK_INTERVAL = 2
RIGHT_CLICK_DELAY = 3
last_right_click_time = 0

class BlinkWinkApp():
    def __init__(self, shared_dict, lock):
        self.shared_dict = shared_dict
        self.lock = lock
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
        self.model_b = load_model('models/blinkdetection.h5')

    def update_shared_dict(self, key, value):
        if self.lock:
            with self.lock:
                self.shared_dict[key] = value

    def detect_blink(self, eye_img, model_b):
        pred_B = model_b.predict(eye_img)
        status = pred_B[0][0]
        status = status * 100
        return round(status, 3)

    def crop_eye(self, gray, eye_points):
        x1, y1 = np.amin(eye_points, axis=0)
        x2, y2 = np.amax(eye_points, axis=0)
        cx, cy = (x1 + x2) / 2, (y1 + y2) / 2
        w = (x2 - x1) * 1.2
        h = w * B_SIZE[1] / B_SIZE[0]

        margin_x, margin_y = w / 2, h / 2
        min_x, min_y = int(cx - margin_x), int(cy - margin_y)
        max_x, max_y = int(cx + margin_x), int(cy + margin_y)
        eye_rect = np.rint([min_x, min_y, max_x, max_y]).astype(int)
        eye_img = gray[eye_rect[1]:eye_rect[3], eye_rect[0]:eye_rect[2]]
        return eye_img, eye_rect

    def handle_left_wink(self):
        global left_wink_start_time
        current_time = time.time()
        if left_wink_start_time and (current_time - left_wink_start_time) <= DOUBLE_CLICK_INTERVAL:
            self.update_shared_dict('msg', 'Double click performed!')
            pyautogui.doubleClick(button="left")
            left_wink_start_time = None
        else:
            self.update_shared_dict('msg', 'Click performed!')
            pyautogui.click(button="left")
            left_wink_start_time = current_time

    def handle_right_wink(self):
        global last_right_click_time
        current_time = time.time()
        if current_time - last_right_click_time >= RIGHT_CLICK_DELAY:
            self.update_shared_dict('msg', 'Right click performed!')
            pyautogui.click(button="right")
            last_right_click_time = current_time

    def handle_scroll_mode(self):
        global scroll_mode
        scroll_mode = not scroll_mode

    def blink_wink_detection(self):
        global blinking_frames
        while self.shared_dict['backend_stat']:
            if self.shared_dict['image']:
                if self.lock:
                    with self.lock:
                        b_gray = self.shared_dict['image'].pop(-1)
                gray = cv2.cvtColor(b_gray, cv2.COLOR_BGR2GRAY)
                faces = self.detector(gray)

                for face in faces:
                    shapes = self.predictor(gray, face)
                    shapes = face_utils.shape_to_np(shapes)
                    eye_img_l, _ = self.crop_eye(gray, eye_points=shapes[36:42])
                    eye_img_r, _ = self.crop_eye(gray, eye_points=shapes[42:48])

                    eye_blink_left = cv2.resize(eye_img_l.copy(), B_SIZE)
                    eye_blink_right = cv2.resize(eye_img_r.copy(), B_SIZE)
                    eye_blink_left_i = eye_blink_left.reshape((1, B_SIZE[1], B_SIZE[0], 1)).astype(np.float32) / 255.
                    eye_blink_right_i = eye_blink_right.reshape((1, B_SIZE[1], B_SIZE[0], 1)).astype(np.float32) / 255.

                    status_l = self.detect_blink(eye_blink_left_i, self.model_b)
                    status_r = self.detect_blink(eye_blink_right_i, self.model_b)

                    if status_r < 50 and status_l < 50:
                        blinking_frames += 1
                        if blinking_frames == frames_to_blink:
                            self.handle_scroll_mode()
                    elif status_l < 5 and status_r >= 20:
                        self.handle_left_wink()
                    elif status_l >= 20 and status_r < 5:
                        self.handle_right_wink()
                    else:
                        blinking_frames = 0
            self.update_shared_dict('msg', 'No action yet')

    def run(self):
        detection_thread = threading.Thread(target=self.blink_wink_detection)
        detection_thread.start()
