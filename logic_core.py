"""Core logic for hand gesture recognition and mouse control."""
import cv2
import mediapipe as mp
from mediapipe.tasks.python import vision, BaseOptions
import math
import time
import numpy as np
from pynput.mouse import Controller as MouseController, Button

from config import (
    MODEL_PATH, SYS_W, SYS_H, ACTIVE_W, ACTIVE_H,
    PINCH_CLICK, PINCH_RELEASE, STABILIZER_TRIGGER,
    SMOOTH_FAST, SMOOTH_SLOW, SCROLL_SENSITIVITY, SCROLL_DEADZONE
)


# Initialize mouse controller
_mouse = MouseController()


def mouse_move(x, y):
    _mouse.position = (x, y)


def mouse_down():
    _mouse.press(Button.left)


def mouse_up():
    _mouse.release(Button.left)


def mouse_right_down():
    _mouse.press(Button.right)


def mouse_right_up():
    _mouse.release(Button.right)


def mouse_scroll(delta):
    # pynput scroll: positive = up, negative = down
    # delta is already in correct sign from our gesture logic
    # Convert pixel delta to scroll "clicks" (arbitrary scale factor)
    scroll_clicks = int(delta / 10)
    if scroll_clicks != 0:
        _mouse.scroll(0, scroll_clicks)


class CyberRender:
    """Renders visual feedback on the video frame."""
    
    def __init__(self):
        self.angle = 0
        self.C_MAIN = (255, 255, 0)
        self.C_ACTIVE = (0, 255, 0)
        self.C_CLICK = (0, 0, 255)
        self.C_PRE = (255, 0, 255)

    def draw_hud(self, img, zone_rect):
        x, y, w, h = zone_rect
        cv2.rectangle(img, (x, y), (x + w, y + h), self.C_ACTIVE, 1)
        # Уголки
        l = 15
        cv2.line(img, (x, y), (x + l, y), self.C_ACTIVE, 3)
        cv2.line(img, (x, y), (x, y + l), self.C_ACTIVE, 3)
        cv2.line(img, (x + w, y + h), (x + w - l, y + h), self.C_ACTIVE, 3)
        cv2.line(img, (x + w, y + h), (x + w, y + h - l), self.C_ACTIVE, 3)
        return img

    def draw_cursor(self, img, x, y, pinch, is_click):
        self.angle = (self.angle + 4) % 360

        if is_click:
            color = self.C_CLICK
            rad = 8
            status = "CLICK"
        elif pinch < STABILIZER_TRIGGER:
            color = self.C_PRE
            rad = 12
            status = "AIMING"
        else:
            color = self.C_MAIN
            rad = 18
            status = "MOVE"

        cv2.circle(img, (x, y), rad, color, 2)
        cv2.circle(img, (x, y), 3, (255, 255, 255), -1)

        if not is_click and pinch < 0.6:
            ring_rad = int(np.interp(pinch, [PINCH_CLICK, 0.6], [rad, rad * 3]))
            cv2.circle(img, (x, y), ring_rad, (100, 100, 100), 1)

        cv2.putText(img, status, (x + 25, y + 5), cv2.FONT_HERSHEY_PLAIN, 1, color, 1)


class LogicCore:
    """Main logic for hand gesture recognition and control."""
    
    def __init__(self):
        options = vision.HandLandmarkerOptions(
            base_options=BaseOptions(model_asset_path=MODEL_PATH),
            running_mode=vision.RunningMode.VIDEO,
            num_hands=1,
            min_hand_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.hands = vision.HandLandmarker.create_from_options(options)
        self.cx, self.cy = 0, 0
        self.clicked = False
        self.right_clicked = False
        self.scroll_active = False
        self.prev_wrist_y = None
        self.init = False
        self._start_time = time.time()

    def process(self, frame, renderer):
        h, w, _ = frame.shape
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
        timestamp_ms = int((time.time() - self._start_time) * 1000)
        res = self.hands.detect_for_video(mp_image, timestamp_ms)

        # 1. Рисуем зону
        zone_w, zone_h = int(w * ACTIVE_W), int(h * ACTIVE_H)
        zone_x, zone_y = int((w - zone_w) / 2), int((h - zone_h) / 2)
        renderer.draw_hud(frame, (zone_x, zone_y, zone_w, zone_h))

        if res.hand_landmarks:
            lm = res.hand_landmarks[0]

            raw_x = lm[5].x
            raw_y = lm[5].y

            x1, y1 = lm[4].x * w, lm[4].y * h
            x2, y2 = lm[8].x * w, lm[8].y * h
            pinch_dist = math.hypot(x2 - x1, y2 - y1)

            x3, y3 = lm[12].x * w, lm[12].y * h
            pinch_dist_right = math.hypot(x3 - x1, y3 - y1)

            x4, y4 = lm[16].x * w, lm[16].y * h
            pinch_dist_scroll = math.hypot(x4 - x1, y4 - y1)

            palm_size = math.hypot(lm[0].x * w - lm[9].x * w, lm[0].y * h - lm[9].y * h)
            pinch = pinch_dist / palm_size
            pinch_right = pinch_dist_right / palm_size
            pinch_scroll = pinch_dist_scroll / palm_size

            target_x = np.interp(raw_x * w, (zone_x, zone_x + zone_w), (0, SYS_W))
            target_y = np.interp(raw_y * h, (zone_y, zone_y + zone_h), (0, SYS_H))

            if not self.init:
                self.cx, self.cy = target_x, target_y
                self.init = True

            if pinch < STABILIZER_TRIGGER:
                alpha = SMOOTH_SLOW
            else:
                dist = math.hypot(target_x - self.cx, target_y - self.cy)
                speed_factor = min(1.0, dist / 150.0)
                alpha = SMOOTH_SLOW - speed_factor * (SMOOTH_SLOW - SMOOTH_FAST)

            self.cx = self.cx * alpha + target_x * (1 - alpha)
            self.cy = self.cy * alpha + target_y * (1 - alpha)

            if not self.clicked:
                if pinch < PINCH_CLICK:
                    self.clicked = True
                    mouse_down()
            else:
                if pinch > PINCH_RELEASE:
                    self.clicked = False
                    mouse_up()

            # Правый клик (большой + средний палец). Срабатывает только когда
            # левый клик не активен в этом кадре, чтобы жесты не конфликтовали.
            if not self.clicked:
                if not self.right_clicked:
                    if pinch_right < PINCH_CLICK:
                        self.right_clicked = True
                        mouse_right_down()
                else:
                    if pinch_right > PINCH_RELEASE:
                        self.right_clicked = False
                        mouse_right_up()
            elif self.right_clicked:
                self.right_clicked = False
                mouse_right_up()

            # Скролл (большой + безымянный палец). Клики имеют приоритет:
            # жест скролла игнорируется, пока активен левый или правый клик.
            wrist_y = lm[0].y * h
            if not self.clicked and not self.right_clicked and pinch_scroll < PINCH_CLICK:
                self.scroll_active = True
                if self.prev_wrist_y is not None:
                    delta_y = wrist_y - self.prev_wrist_y
                    if abs(delta_y) > SCROLL_DEADZONE:
                        mouse_scroll(delta_y * SCROLL_SENSITIVITY)
                self.prev_wrist_y = wrist_y
            else:
                self.scroll_active = False
                self.prev_wrist_y = wrist_y

            mouse_move(int(self.cx), int(self.cy))

            vis_x, vis_y = int(lm[8].x * w), int(lm[8].y * h)
            renderer.draw_cursor(frame, vis_x, vis_y, pinch, self.clicked or self.right_clicked)

        else:
            self.init = False
            self.scroll_active = False
            self.prev_wrist_y = None
            cv2.putText(frame, "NO HAND", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        return frame
