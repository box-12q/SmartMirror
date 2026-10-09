import sys
import cv2
import mediapipe as mp
import math
import time
import ctypes
import numpy as np
from collections import deque
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QLabel,
                             QVBoxLayout, QHBoxLayout, QPushButton, QFrame,
                             QGraphicsDropShadowEffect)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QPoint
from PyQt6.QtGui import QImage, QPixmap, QColor, QFont


user32 = ctypes.windll.user32
user32.SetProcessDPIAware()
SYS_W, SYS_H = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

CAM_INDEX = 0


ACTIVE_W = 0.50
ACTIVE_H = 0.40


PINCH_CLICK = 0.20
PINCH_RELEASE = 0.28
STABILIZER_TRIGGER = 0.40


SMOOTH_FAST = 0.15
SMOOTH_SLOW = 0.92


def mouse_move(x, y):
    nx = int(x * 65535 / (SYS_W - 1))
    ny = int(y * 65535 / (SYS_H - 1))
    user32.mouse_event(0x8001, nx, ny, 0, 0)


def mouse_down(): user32.mouse_event(0x0002, 0, 0, 0, 0)


def mouse_up():   user32.mouse_event(0x0004, 0, 0, 0, 0)


class CyberRender:
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
    def __init__(self):
        self.hands = mp.solutions.hands.Hands(
            max_num_hands=1,
            model_complexity=0,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.cx, self.cy = 0, 0
        self.clicked = False
        self.init = False

    def process(self, frame, renderer):
        h, w, _ = frame.shape
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        res = self.hands.process(rgb)

        # 1. Рисуем зону
        zone_w, zone_h = int(w * ACTIVE_W), int(h * ACTIVE_H)
        zone_x, zone_y = int((w - zone_w) / 2), int((h - zone_h) / 2)
        renderer.draw_hud(frame, (zone_x, zone_y, zone_w, zone_h))

        if res.multi_hand_landmarks:
            lm = res.multi_hand_landmarks[0].landmark


            raw_x = lm[5].x
            raw_y = lm[5].y

            x1, y1 = lm[4].x * w, lm[4].y * h
            x2, y2 = lm[8].x * w, lm[8].y * h
            pinch_dist = math.hypot(x2 - x1, y2 - y1)

            palm_size = math.hypot(lm[0].x * w - lm[9].x * w, lm[0].y * h - lm[9].y * h)
            pinch = pinch_dist / palm_size


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


            mouse_move(int(self.cx), int(self.cy))


            vis_x, vis_y = int(lm[8].x * w), int(lm[8].y * h)
            renderer.draw_cursor(frame, vis_x, vis_y, pinch, self.clicked)

        else:
            self.init = False
            cv2.putText(frame, "NO HAND", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        return frame


class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(QImage)
    status_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self._run_flag = True

    def run(self):
        cap = cv2.VideoCapture(CAM_INDEX, cv2.CAP_DSHOW)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        cap.set(cv2.CAP_PROP_FPS, 60)

        renderer = CyberRender()
        core = LogicCore()

        self.status_signal.emit("RABOTAI // POZALUSTA")

        while self._run_flag:
            ret, frame = cap.read()
            if ret:
                frame = cv2.flip(frame, 1)
                frame = core.process(frame, renderer)

                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgb.shape
                qt_img = QImage(rgb.data, w, h, ch * w, QImage.Format.Format_RGB888)
                p = qt_img.scaled(960, 540, Qt.AspectRatioMode.KeepAspectRatio)
                self.change_pixmap_signal.emit(p)
            else:
                break
        cap.release()

    def stop(self):
        self._run_flag = False
        self.wait()



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.resize(1000, 650)

        self.central = QWidget()
        self.setCentralWidget(self.central)
        self.layout = QVBoxLayout(self.central)


        self.bg = QFrame()
        self.bg.setStyleSheet("background: #0b0b10; border: 2px solid #00ffaa; border-radius: 10px;")
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(0, 255, 170, 80))
        self.bg.setGraphicsEffect(shadow)

        self.inner = QVBoxLayout(self.bg)


        self.title_bar = QHBoxLayout()
        self.lbl_title = QLabel("GLAZA_GRISHI")
        self.lbl_title.setStyleSheet("color: #00ffaa; font-family: Consolas; font-weight: bold;")
        self.btn_exit = QPushButton("X")
        self.btn_exit.setFixedSize(30, 30)
        self.btn_exit.clicked.connect(self.close)
        self.btn_exit.setStyleSheet("background: transparent; color: red; border: 1px solid red; border-radius: 5px;")

        self.title_bar.addWidget(self.lbl_title)
        self.title_bar.addStretch()
        self.title_bar.addWidget(self.btn_exit)
        self.inner.addLayout(self.title_bar)

        # Видео
        self.display = QLabel()
        self.display.setFixedSize(960, 540)
        self.display.setStyleSheet("background: #000; border: 1px solid #222;")
        self.display.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.inner.addWidget(self.display, alignment=Qt.AlignmentFlag.AlignCenter)

        # Статус
        self.lbl_stat = QLabel("INIT")
        self.lbl_stat.setStyleSheet("color: #aaa; font-family: Consolas;")
        self.inner.addWidget(self.lbl_stat)

        self.layout.addWidget(self.bg)

        # Логика окна
        self.old_pos = None

        # Запуск камеры
        self.thread = VideoThread()
        self.thread.change_pixmap_signal.connect(lambda x: self.display.setPixmap(QPixmap.fromImage(x)))
        self.thread.status_signal.connect(self.lbl_stat.setText)
        self.thread.start()

    def mousePressEvent(self, event): self.old_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if self.old_pos:
            delta = event.globalPosition().toPoint() - self.old_pos
            self.move(self.pos() + delta)
            self.old_pos = event.globalPosition().toPoint()

    def mouseReleaseEvent(self, e): self.old_pos = None

    def closeEvent(self, e): self.thread.stop()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())